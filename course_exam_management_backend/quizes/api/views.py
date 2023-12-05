import ast

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from quizes.api.serializers import QuizSerializer, QuizMcqsSerializer, QuizPythonProblemSerializer, \
    DeliveredQuizMcqsSerializer, DeliveredQuizSerializer, DeliveredQuizWriteOnlySerializer
from quizes.filters import DeliveredQuizApiFilter
from quizes.models import QuizMcqs, Quiz, QuizPythonProblem, QuizPythonProblemTestCase, DeliveredQuizMcqs, DeliveredQuiz
import subprocess

from django.conf import settings


class QuizViewSet(ModelViewSet):
    serializer_class = QuizSerializer
    model = Quiz
    queryset = Quiz.objects.all()


class DeliveredQuizViewSet(ModelViewSet):
    serializer_class = DeliveredQuizSerializer
    model = DeliveredQuiz
    queryset = DeliveredQuiz.objects.all()
    filterset_class = DeliveredQuizApiFilter


class CompilePythonCodeAPIView(APIView):

    def post(self, request, format=None):
        original_code = request.data.get('code')

        code = original_code
        result = []
        output = ''
        if request.data.get('code'):
            for test_case in request.data.get('test_cases'):
                user_added_print_statement = False
                code = original_code
                input_list = test_case.get('text').split("\n")
                for inp in input_list:
                    code = code.replace("input()", str(inp), 1)

                code = code.replace("input()", str())
                try:
                    tree = ast.parse(code)
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

                # Find the last expression in the if block
                last_expr = None
                for stmt in tree.body:
                    if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare) and len(stmt.test.ops) == 1:
                        if isinstance(stmt.test.ops[0], ast.Eq) and isinstance(stmt.test.left,
                                                                               ast.Name) and stmt.test.left.id == "__name__":
                            if isinstance(stmt.test.comparators[0], ast.Constant) and stmt.test.comparators[
                                0].value == "__main__":
                                for expr in stmt.body:
                                    if isinstance(expr, ast.Expr):
                                        last_expr = expr

                # If we found a last expression, wrap it in a print statement
                if last_expr:
                    if isinstance(last_expr.value, ast.Call) and isinstance(last_expr.value.func,
                                                                            ast.Name) and last_expr.value.func.id == "print":
                        print("The last expression is already a print statement")
                        # The last expression is already a print statement
                        user_added_print_statement = True
                    print_call = ast.Call(func=ast.Name(id="print", ctx=ast.Load()),
                                          args=[last_expr.value],
                                          keywords=[])

                    print_expr = ast.Expr(value=print_call)
                    stmt_idx = tree.body.index(stmt)
                    tree.body[stmt_idx].body[-1] = print_expr

                    # Generate the new code
                    code = ast.unparse(tree)
                else:
                    print("No expression found")
                    return Response(
                        {"error": "No assign the final answer into the any variable. Just write the final Result"},
                        status=status.HTTP_400_BAD_REQUEST)

                try:
                    exec(code)
                    # exec(request.data.get('code'))
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                # Write the code to a temporary file

                with open(str(settings.MEDIA_ROOT) + '\\' + test_case.get('name', '') + str(
                        test_case.get('id', '')) + ".py",
                          'w') as f:
                    f.write(code)

                # Run the code using subprocess and capture the output
                try:
                    compile_output = subprocess.check_output(
                        ['python', str(settings.MEDIA_ROOT) + '\\' + test_case.get('name', '') + str(
                            test_case.get('id', '')) + ".py"],
                        stderr=subprocess.STDOUT,
                        text=True)

                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                print(compile_output.split('\n'))
                if test_case.get('correct_answer').lower() == (
                compile_output.split('\n')[-3].lower() if user_added_print_statement else compile_output.split('\n')[
                    -2].lower()):
                    # test_case['result'] = True
                    result.append({
                        'test_case': test_case.get('id'),
                        'test_case_name': test_case.get('name'),
                        'answer': compile_output.split('\n')[-3].lower() if user_added_print_statement else
                        compile_output.split('\n')[-2].lower(),
                        'numbers': test_case.get('numbers'),
                        'total_number': test_case.get('numbers'),
                        'is_correct_answer': True,
                        'quiz_python_problem': test_case.get('quiz_python_problem'),
                    })
                else:
                    # test_case['result'] = False
                    result.append({
                        'test_case': test_case.get('id'),
                        'test_case_name': test_case.get('name'),
                        'answer': compile_output.split('\n')[-3].lower() if user_added_print_statement else
                        compile_output.split('\n')[-2].lower(),
                        'numbers': 0,
                        'total_number': test_case.get('numbers'),
                        'is_correct_answer': False,
                        'quiz_python_problem': test_case.get('quiz_python_problem'),
                    })
                # print(compile_output)
                # print(compile_output.split('\n'))
                # print("\n".join(compile_output.split('\n')[:-2]))
                output = output + "\n".join(
                    compile_output.split('\n')[:-2]) if not user_added_print_statement else compile_output

                # print(output)
                # output = subprocess.check_output(['python', 'temp_script.py'], stderr=subprocess.STDOUT,
                #                                  text=True)
            # print(output)
            print(result)

            return Response({"output": output, "results": result},
                            status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                exec(code)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeliveredQuizCreateApiView(ModelViewSet):
    serializer_class = DeliveredQuizWriteOnlySerializer
    model = DeliveredQuiz
    queryset = DeliveredQuiz.objects.all()
