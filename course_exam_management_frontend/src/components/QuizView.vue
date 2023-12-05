<template>
    <v-container>
        <QuizResult v-if="coursesResult.length!==0" :quiz-results="coursesResult" class="mb-3"/>
        <AvailiableQuiz v-if="quizes.length!==0" :quizes="quizes"/>

        <v-card class="mx-2 mt-3" v-if="isQuizSelected">
            <v-card-title class="headline font-weight-bold text-uppercase">{{ selectedQuiz.name }}</v-card-title>
            <v-card-text>
                <v-container v-for="(item, index) in mcqsQuizes" :key="item">
                    <p class="body-1">
                        <strong>{{ index + 1 }}. </strong>
                        {{ item.question }}
                    </p>
                    <v-radio-group @change="onAnswerSelected($event,item)" v-model="selectedAnswers[item.id]"
                                   v-if="item.correct_answers.length===1">
                        <v-radio :label="item.option1" :value="item.option1"></v-radio>
                        <v-radio :label="item.option2" :value="item.option2"></v-radio>
                        <v-radio :label="item.option3" :value="item.option3"></v-radio>
                        <v-radio :label="item.option4" :value="item.option4"></v-radio>
                    </v-radio-group>
                    <div v-else>
                        <v-row>
                            <v-checkbox-btn
                                    :label="item.option1"
                                    :value="item.option1"
                                    class="v-col-12"
                                    @change="onMultipleAnswerSelected($event,item,'option1')"
                            >
                            </v-checkbox-btn>
                            <v-checkbox-btn
                                    :label="item.option2"
                                    :value="item.option2"
                                    class="v-col-12"
                                    @change="onMultipleAnswerSelected($event,item,'option2')"
                            >
                            </v-checkbox-btn>
                            <v-checkbox-btn
                                    :label="item.option3"
                                    :value="item.option3"
                                    class="v-col-12"
                                    @change="onMultipleAnswerSelected($event,item,'option3')"
                            >
                            </v-checkbox-btn>
                            <v-checkbox-btn
                                    :label="item.option4"
                                    :value="item.option4"
                                    class="v-col-12"
                                    @change="onMultipleAnswerSelected($event,item,'option4')"
                            >
                            </v-checkbox-btn>
                        </v-row>
                    </div>

                    <v-divider></v-divider>
                </v-container>
                <v-container>

                    <v-dialog
                            v-model="createPythonQuizDialog"
                            fullscreen
                            :scrim="false"
                            transition="dialog-bottom-transition"
                    >
                        <template v-slot:activator="{ props }">
                            <v-btn
                                    color="#dc899e"
                                    dark
                                    v-bind="props"
                                    @click="createPythonQuizDialog=true"
                                    v-if="pythonQuizes.length!==0"
                            >
                                Start Python Quiz
                            </v-btn>

                        </template>
                        <v-card>
                            <v-toolbar
                                    dark
                                    color="#dc899e"
                            >
                                <v-btn
                                        icon
                                        dark
                                        @click="createPythonQuizDialog=false"
                                >
                                    <v-icon>mdi-close</v-icon>
                                </v-btn>
                                <v-toolbar-title>Quiz</v-toolbar-title>
                                <v-spacer></v-spacer>

                            </v-toolbar>
                            <PythonQuizView :python-problem="pythonQuizes" class="mx-2 mt-2"/>

                        </v-card>
                    </v-dialog>
                </v-container>
                <v-spacer></v-spacer>
                <v-btn color="#dc899e" @click="submitQuiz">Submit Quiz</v-btn>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script>
import {api} from "@/utils/axios";
import router from "@/router";
import {mapGetters} from "vuex";
import Form from "@/utils/form";
import PythonQuizView from "@/components/PythonQuizView.vue";
import QuizResult from "@/components/QuizResult.vue";
import PythonCompiler from "@/components/PythonCompiler.vue";
import AvailiableQuiz from "@/components/AvailiableQuiz.vue";


export default {
    name: "QuizView",
    components: {AvailiableQuiz, PythonCompiler, QuizResult, PythonQuizView},
    data() {
        return {
            createPythonQuizDialog: false,
            isQuizSelected: false,
            selectedQuiz: {},
            selectedAnswers: [],
            mcqsQuizes: [],
            pythonQuizes: [],
            solvedQuiz: new Form({
                quiz: null,
                course: parseInt(this.$route.params.id),
                student: null,
                deliveredquizmcqs: [],
                deliveredquizpython: []
            }),
            coursesResult: [],
            quizes: [],

        }
    },
    methods: {
        getQuizes() {
            api.get('/get-all-courses/?id=' + this.$route.params.id).then(response => {
                // this.quizes = response.data.length !== 0 ? response.data[0].quiz : []
                this.quizes = response.data
                // this.mcqsQuizes = response.data.quizmcqs_set
                // this.pythonQuizes = response.data.quizpythonproblem_set
            })
        },
        onAnswerSelected(event, option) {
            let deduct_number = option.correct_answers[0].numbers
            let index = this.solvedQuiz['deliveredquizmcqs'].findIndex(obj => obj.mcqs_quiz === option.id);
            if (index !== -1) {
                this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[0].answer = event.target.value;
                this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[0].is_correct_answer = option.correct_answers[0].correct_answer === event.target.value ? true : false;
                // this.solvedQuiz['deliveredquizmcqs'][index].answer = this.selectedAnswers[option.id];
                // this.solvedQuiz['deliveredquizmcqs'][index].is_correct_answer = this.selectedAnswers[option.id] == option.correct_answer ? true : false
                this.solvedQuiz['deliveredquizmcqs'][index].numbers = this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[0].is_correct_answer ? option.correct_answers[0].numbers : 0
            } else {

                this.solvedQuiz['deliveredquizmcqs'].push({
                    mcqs_quiz: option.id,
                    // answer: this.selectedAnswers[option.id],
                    // is_correct_answer: this.selectedAnswers[option.id] == option.correct_answer ? true : false,
                    // numbers: this.selectedAnswers[option.id] == option.correct_answer ? option.numbers : 0
                    numbers: option.correct_answers[0].correct_answer === event.target.value ? option.correct_answers[0].numbers : 0,
                    mcqs_answers: [
                        {
                            answer: event.target.value,
                            is_correct_answer: option.correct_answers[0].correct_answer === event.target.value ? true : false,
                            number: deduct_number,
                        }
                    ],

                });
            }

        },
        onMultipleAnswerSelected(event, option, option_val) {
            let deduct_number = option.correct_answers[0].numbers

            console.log(option)
            let index = this.solvedQuiz['deliveredquizmcqs'].findIndex(obj => obj.mcqs_quiz === option.id);
            if (index !== -1) {
                // this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[0].answer = event.target.value;
                let optIndex = this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.findIndex(obj => obj.option === option_val);
                console.log(optIndex)
                if (optIndex !== -1) {
                    console.log(this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[optIndex])
                    this.solvedQuiz['deliveredquizmcqs'][index].numbers -= this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[optIndex].number
                    this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.splice(optIndex, 1)
                } else {
                    const ind = option.correct_answers.findIndex(ans => ans.correct_answer === event.target.value)
                    console.log(ind)
                    if (ind !== -1) {
                        this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.push(
                            {
                                answer: event.target.value,
                                is_correct_answer: true,
                                number: deduct_number,
                                option: option_val,
                            }
                        )
                    } else {
                        this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.push(
                            {
                                answer: event.target.value,
                                is_correct_answer: false,
                                number: deduct_number,
                                option: option_val,
                            }
                        )
                    }

                    // let correct_answer_total_number = 0
                    // let false_answer_total_number = 0
                    // this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.forEach(mcqs => {
                    //     if (mcqs.is_correct_answer) {
                    //         correct_answer_total_number += mcqs.number
                    //     }
                    // })
                    //
                    // this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.forEach(mcqs => {
                    //     if (!mcqs.is_correct_answer) {
                    //         false_answer_total_number += 1
                    //     }
                    // })
                    // let number = 0
                    // if (ind !== -1) {
                    //     this.solvedQuiz['deliveredquizmcqs'][index].numbers = this.solvedQuiz['deliveredquizmcqs'][index].numbers / 2
                    // }
                    // else {
                    //     number = 0 - this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers[this.solvedQuiz['deliveredquizmcqs'][index].mcqs_answers.length - 1].number
                    //     console.log(number)
                    // }


                }
            } else {
                const ind = option.correct_answers.findIndex(ans => ans.correct_answer === event.target.value)
                console.log(ind)
                this.solvedQuiz['deliveredquizmcqs'].push({
                    mcqs_quiz: option.id,
                    numbers: ind !== -1 ? option.correct_answers[ind].numbers : 0,
                    mcqs_answers: [
                        {
                            answer: event.target.value,
                            is_correct_answer: ind !== -1 ? true : false,
                            number: ind !== -1 ? option.correct_answers[ind].numbers : 0,
                            option: option_val,
                        }
                    ],

                });
            }
        },
        submitQuiz() {
            this.solvedQuiz.student = this.fetchMe.id

            this.solvedQuiz.deliveredquizpython = this.getPythonQuizSolution
            this.solvedQuiz.submit('post', '/delivered_quiz/').then(response => {
                this.mcqsQuizes = []
                this.pythonQuizes = []
                this.solvedQuiz.quiz = null
                this.isQuizSelected = false
                this.selectedQuiz = {}
                this.getQuizes()
                this.getQuizResult()
            }).catch(error => {

            })
        },
        getQuizResult() {
            api.get('/delivered_quiz/?course__id=' + this.$route.params.id + '&student__id=' + this.fetchMe.id).then(response => {
                this.coursesResult = response.data

            }).catch(error => {

            })
        }
    },
    computed: {
        ...mapGetters([
            'fetchMe',
            'getPythonQuizSolution',
        ])

    },

    mounted() {
        this.getQuizes()
        this.getQuizResult()

    },
    created() {
        this.emitter.on("quiz-selected", (quiz) => {
            console.log(quiz)
            this.mcqsQuizes = quiz.quizmcqs_set
            this.pythonQuizes = quiz.quizpythonproblem_set
            this.solvedQuiz.quiz = quiz.id
            this.isQuizSelected = true
            this.selectedQuiz = quiz
        })
    }
}
</script>

<style scoped>

</style>
