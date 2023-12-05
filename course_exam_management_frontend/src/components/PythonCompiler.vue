<template>
    <v-card>
        <v-container>
        <vue-monaco-editor
                    v-model:value="form.code"
                    theme="vs-dark"
                    style="height: 500px"
            />
            <h4 class="mt-3">Output</h4>
            <div class="mt-3" v-if="code_output!==null">
                <p class="ml-4" v-for="output in code_output.split('\n')">
                    <span v-if="output!='None'">{{ output }}</span>
                </p>
            </div>
            <v-row class="mt-3" v-else>
                <p class="ml-4" style="color: red">{{ error }}</p>
            </v-row>
            <v-row class="m-3">
                <v-btn color="#ce5a94" @click="compilePythonCode" class="mt-4">Compile</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="#ce5a5a" @click="runTestCases" class="mt-4" :disabled="test_case_results.length!==0">Run
                    Test Cases
                </v-btn>
            </v-row>
            <v-table v-if="test_case_results.length!==0">
                <thead>
                <tr>
                    <th class="text-left">
                        Test Case
                    </th>
                    <th class="text-left">
                        Correct Answer
                    </th>
                    <th class="text-left">
                        Total Score
                    </th>
                    <th class="text-left">
                        Award Score
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr
                        v-for="test_case in test_case_results"
                        :key="test_case.name"
                >
                    <td>{{ test_case.test_case_name }}</td>
                    <td>{{ test_case.is_correct_answer }}</td>
                    <td>{{ test_case.total_number }}</td>
                    <td>{{ test_case.numbers }}</td>
                </tr>
                </tbody>
            </v-table>


        </v-container>
    </v-card>
</template>

<script>
import Form from "@/utils/form";
import store from "@/store";
import {mapGetters} from "vuex";
import {eventBus} from "@/utils/eventBus";

export default {
    name: "PythonCompiler",
    props: ["selectedQuiz"],
    data() {
        return {
            form: new Form({
                code: '',
                test_cases: []
            }),
            error: null,
            code_output: null,
            code: null,
            test_case_results: []
        }
    },
    methods: {
        compilePythonCode() {
            this.error = null
            this.code_output = null
            this.code = this.form.code
            this.form.test_cases = this.selectedQuiz.test_case
            this.form.post('/compile_python/').then(response => {
                console.log(response)
                this.code_output = response.output
                this.form.code = this.code
                // this.test_case_results = response.results
                // this.save()
            }).catch(error => {
                console.log(error)
                this.error = error.data.error
                // this.save()
            })
        },
        runTestCases() {
            this.error = null
            this.code_output = null
            this.code = this.form.code
            this.form.test_cases = this.selectedQuiz.test_case
            this.form.post('/compile_python/').then(response => {
                console.log(response)
                this.code_output = response.output
                this.form.code = this.code
                this.test_case_results = response.results
                this.save()
                eventBus.emit('savePythonTest')
            }).catch(error => {
                console.log(error)
                this.error = error.data.error
                this.save()
                eventBus.emit('savePythonTest')
            })
        },
        save() {
            let index = this.getPythonQuizSolution.findIndex(obj => obj.quiz_python_problem === this.selectedQuiz.id);
            console.log(index)
            if (index !== -1) {
                this.selectedQuiz['code']
                this.getPythonQuizSolution[index] = {
                    "quiz_python_problem": this.selectedQuiz.id,
                    "correct_answer": this.selectedQuiz.correct_answer,
                    "total_number": this.selectedQuiz.numbers,
                    "code": this.form.code,
                    "answer": this.code_output,
                    "error": this.error,
                    "test_cases": this.test_case_results,
                }
            } else {
                this.getPythonQuizSolution.push({
                    "quiz_python_problem": this.selectedQuiz.id,
                    "correct_answer": this.selectedQuiz.correct_answer,
                    "total_number": this.selectedQuiz.numbers,
                    "code": this.form.code,
                    "answer": this.code_output,
                    "error": this.error,
                    "test_cases": this.test_case_results,
                })
            }
            store.commit("setPythonQuizSolution", this.getPythonQuizSolution)
        },

    },
    computed: {
        ...mapGetters([
            'getPythonQuizSolution',
        ])
    },
    watch: {
        selectedQuiz: function (newVal, oldVal) { // watch it
            if (newVal) {
                console.log(newVal)
                let index = this.getPythonQuizSolution.findIndex(obj => obj.quiz_python_problem === newVal.quiz_python_problem);
                if (index !== -1) {
                    this.form.code = this.getPythonQuizSolution[index].code
                    this.code_output = this.getPythonQuizSolution[index].answer
                    this.error = this.getPythonQuizSolution[index].error
                } else {
                    this.form.code = ''
                    this.code_output = null
                    this.error = null
                }
            }
        }
    },
    mounted() {
        console.log(this.selectedQuiz)
        // console.log(this.getPythonQuizSolution)
        let index = this.getPythonQuizSolution.findIndex(obj => obj.quiz_python_problem === this.selectedQuiz.id);
        if (index !== -1) {
            this.form.code = this.getPythonQuizSolution[index].code
            this.code_output = this.getPythonQuizSolution[index].answer
            this.error = this.getPythonQuizSolution[index].error
            this.test_case_results = this.getPythonQuizSolution[index].test_cases
        } else {
            this.form.code = this.selectedQuiz.sample_code
        }

    }
}
</script>

<style scoped>

</style>
