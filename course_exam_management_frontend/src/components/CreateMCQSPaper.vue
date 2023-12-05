<template>
    <v-container>
        <v-row>
            <h3>Multiple-choice questions</h3>
        </v-row>
        <div v-for="(question,index) in mcqsQuestions" class="mt-3">
            <v-row>
                <v-col cols="10">
                    <v-textarea
                            label="Question"
                            rows="3"
                            v-model="mcqsQuestions[index].question"
                            density="compact"
                    ></v-textarea>
                </v-col>
            </v-row>
            <v-row class="mt-3">
                <v-col cols="3">
                    <v-textarea
                            label="Option 1"
                            rows="1"
                            v-model="mcqsQuestions[index].option1"
                            @input="optionValueChange(index)"
                            density="compact"
                    ></v-textarea>
                </v-col>
                <v-col cols="3">
                    <v-textarea
                            label="Option 2"
                            no-resize
                            rows="1"
                            v-model="mcqsQuestions[index].option2"
                            @input="optionValueChange(index)"
                            density="compact"
                    ></v-textarea>
                </v-col>
                <v-col cols="3">
                    <v-textarea
                            label="Option 3"
                            no-resize
                            rows="1"
                            v-model="mcqsQuestions[index].option3"
                            @input="optionValueChange(index)"
                            density="compact"
                    ></v-textarea>
                </v-col>
                <v-col cols="3">
                    <v-textarea
                            label="Option 4"
                            no-resize
                            rows="1"
                            v-model="mcqsQuestions[index].option4"
                            @input="optionValueChange(index)"
                            density="compact"
                    ></v-textarea>
                </v-col>
                <v-col cols="9">
                    <v-text-field
                            label="Total Number"
                            v-model="mcqsQuestions[index].total_numbers"
                            density="compact"
                    ></v-text-field>
                </v-col>
                <div cols="12">
                    <h5>Correct Answers</h5>
                    <v-row>
                        <div class="d-flex">
                            <v-checkbox-btn
                                    v-model="mcqsQuestions[index].correct_answers[0].option1"
                                    class="v-col-8"
                                    @change="mcqsAnswerChanged(index,0,mcqsQuestions[index].option1)"
                                    label="Option 1"
                            >
                            </v-checkbox-btn>

                            <v-checkbox-btn
                                    v-model="mcqsQuestions[index].correct_answers[1].option2"
                                    class="v-col-8"
                                    @change="mcqsAnswerChanged(index,1,mcqsQuestions[index].option2)"
                                    label="Option 2"
                            >
                            </v-checkbox-btn>

                        </div>

                    </v-row>
                    <v-row>
                        <div class="d-flex">

                            <v-checkbox-btn
                                    v-model="mcqsQuestions[index].correct_answers[2].option3"
                                    class="v-col-8"
                                    @change="mcqsAnswerChanged(index,2,mcqsQuestions[index].option3)"
                                    label="Option 3"
                            >
                            </v-checkbox-btn>

                            <v-checkbox-btn
                                    v-model="mcqsQuestions[index].correct_answers[3].option4"
                                    class="v-col-8"
                                    @change="mcqsAnswerChanged(index,3,mcqsQuestions[index].option4)"
                                    label="Option 4"
                            >
                            </v-checkbox-btn>
                        </div>
                    </v-row>

                </div>

            </v-row>
            <v-row class="mt-2 mb-2">
                <v-btn density="compact" color="#ce5a5a" @click="deleteQuestion(index)">Delete</v-btn>
            </v-row>
            <v-divider class="mt-2"></v-divider>
        </div>

        <v-row class="mt-2" justify="end">
            <v-btn density="compact" color="#dc899e" @click="addQuestion">Add Question</v-btn>
        </v-row>

    </v-container>
</template>

<script>
import {eventBus} from "@/utils/eventBus";

export default {
    name: "CreateMCQSPaper",

    props: ["updatedQuizmcqs"],
    data() {
        return {
            mcqsQuestions: [
                {
                    question: "",
                    option1: "",
                    option2: "",
                    option3: "",
                    option4: "",
                    correct_answers: [
                        {
                            option1: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option2: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option3: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option4: false,
                            numbers: 0,
                            correct_answer: "",
                        }
                    ],
                    total_numbers: 0,
                }
            ]
        }
    },
    methods: {
        addQuestion() {
            this.mcqsQuestions.push({
                question: "",
                option1: "",
                option2: "",
                option3: "",
                option4: "",
                correct_answers: [
                    {
                        option1: false,
                        numbers: 0,
                        correct_answer: "",
                    },
                    {
                        option2: false,
                        numbers: 0,
                        correct_answer: "",
                    },
                    {
                        option3: false,
                        numbers: 0,
                        correct_answer: "",
                    },
                    {
                        option4: false,
                        numbers: 0,
                        correct_answer: "",
                    }
                ],
                total_numbers: 0,
            })
        },
        deleteQuestion(ind) {
            this.mcqsQuestions.splice(ind, 1);
        },
        mcqsAnswerChanged(mcqsIndex, index, answer) {
            console.log(answer)
            if (this.mcqsQuestions[mcqsIndex].correct_answers[index].option1 || this.mcqsQuestions[mcqsIndex].correct_answers[index].option2 || this.mcqsQuestions[mcqsIndex].correct_answers[index].option3 || this.mcqsQuestions[mcqsIndex].correct_answers[index].option4) {
                this.mcqsQuestions[mcqsIndex].correct_answers[index].correct_answer = answer
            } else {
                this.mcqsQuestions[mcqsIndex].correct_answers[index].correct_answer = ""
            }
        },
        optionValueChange(ind) {
            console.log(ind)
            this.mcqsQuestions[ind].correct_answers = [
                {
                    option1: false,
                    numbers: 0,
                    correct_answer: "",
                },
                {
                    option2: false,
                    numbers: 0,
                    correct_answer: "",
                },
                {
                    option3: false,
                    numbers: 0,
                    correct_answer: "",
                },
                {
                    option4: false,
                    numbers: 0,
                    correct_answer: "",
                }
            ]
        }
    },

    mounted() {
        if (this.updatedQuizmcqs.length !== 0) {
            this.mcqsQuestions = this.updatedQuizmcqs
            this.mcqsQuestions.forEach((mcqs, mcqsIndex) => {
                mcqs.correct_answers.forEach((correct_answer, index) => {
                    console.log(correct_answer)
                    this.mcqsQuestions[mcqsIndex].correct_answers[index]['option' + (index + 1)] = correct_answer.correct_answer.length !== 0 ? true : false
                })
            })

        }

    },
    created() {
        this.emitter.on("send-quiz-data", (message) => {
            this.emitter.emit("updated-mcqs", this.mcqsQuestions)
        })
        this.emitter.on("quiz-created_successfully", (message) => {
            this.mcqsQuestions = [
                {
                    question: "",
                    option1: "",
                    option2: "",
                    option3: "",
                    option4: "",
                    correct_answers: [
                        {
                            option1: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option2: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option3: false,
                            numbers: 0,
                            correct_answer: "",
                        },
                        {
                            option4: false,
                            numbers: 0,
                            correct_answer: "",
                        }
                    ],
                    total_numbers: 0,
                }
            ]
        })


    }
}
</script>

<style scoped>

</style>
