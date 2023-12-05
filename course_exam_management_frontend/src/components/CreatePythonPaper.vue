<template>
    <v-container>
        <v-row>
            <h3>Python Questions</h3>
        </v-row>
        <div v-for="(question,index) in pythonQuestions" class="mt-3">
            <v-row>
                <v-col cols="10">
                    <v-textarea
                            label="Question"
                            rows="1"
                            v-model="pythonQuestions[index].question"
                            density="compact"
                    ></v-textarea>
                </v-col>
                <v-col cols="10">
                    <v-textarea
                        label="Add Start Up Code"
                        rows="2"
                        v-model="pythonQuestions[index].sample_code"
                        density="compact"
                    ></v-textarea>
                </v-col>
            </v-row>
            <v-row class="mt-3">

            </v-row>
            <v-container>
                <v-row>
                    <h3>Test Case</h3>
                </v-row>
                <div v-for="(test,test_index) in pythonQuestions[index].test_case" class="mt-3">
                    <v-row>
                        <v-col cols="6">
                            <v-textarea
                                    label="Test Case Name"
                                    rows="1"
                                    v-model="pythonQuestions[index].test_case[test_index].name"
                                    density="compact"
                            ></v-textarea>
                        </v-col>
                        <v-col cols="6">
                            <v-textarea
                                    label="Enter Input Values"
                                    rows="2"
                                    v-model="pythonQuestions[index].test_case[test_index].text"
                                    density="compact"
                            ></v-textarea>
                        </v-col>
                    </v-row>
                    <v-row class="mt-3">

                        <v-col cols="6">
                            <v-textarea
                                    label="Correct Answer"
                                    no-resize
                                    rows="1"
                                    v-model="pythonQuestions[index].test_case[test_index].correct_answer"
                                    density="compact"
                            ></v-textarea>
                        </v-col>
                        <v-col cols="3">
                            <v-textarea
                                    label="Total Number"
                                    no-resize
                                    rows="1"
                                    v-model="pythonQuestions[index].test_case[test_index].numbers"
                                    density="compact"
                            ></v-textarea>
                        </v-col>

                    </v-row>
                    <v-row class="mt-2 mb-2">
                        <v-btn density="compact" color="#ce5a5a" @click="deleteTestCase(index,test_index)">Delete Test
                            Case
                        </v-btn>
                    </v-row>
                    <v-divider class="mt-2"></v-divider>
                </div>

                <v-row class="mt-2" justify="end">
                    <v-btn density="compact" color="#ce5a94" @click="addTestCase(index)">Add Test Case</v-btn>
                </v-row>
            </v-container>

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
export default {
    name: "CreatePythonPaper",
    props: ["updatedQuizpython"],
    data() {
        return {
            pythonQuestions: [
                // {
                //     question: "",
                //     correct_answer: "",
                //     numbers: null,
                //     test_case: [
                //         {
                //             text: "Python Question Test Case",
                //             correct_answer: "Python Question Test Case Correct Answer",
                //             numbers: 15,
                //         }
                //     ]
                // }
            ]
        }
    },
    methods: {
        addQuestion(index) {
            this.pythonQuestions.push({
                question: "",
                sample_code: "",
                correct_answer: "",
                numbers: null,
                test_case: [
                    {
                        name: "",
                        text: "",
                        correct_answer: "",
                        numbers: null,
                    }
                ]
            })

        },
        deleteQuestion(ind) {
            this.pythonQuestions.splice(ind, 1);
        },

        addTestCase(index) {
            this.pythonQuestions[index].test_case.push({
                text: "",
                correct_answer: "",
                numbers: null,
            })
        },
        deleteTestCase(mcqsInd, ind) {
            this.pythonQuestions[mcqsInd].test_case.splice(ind, 1);
        }

    },
    mounted() {
        if (this.updatedQuizpython.length !== 0) {
            this.pythonQuestions = this.updatedQuizpython
        }
    },
    created() {
        this.emitter.on("send-quiz-data", (message) => {
            this.emitter.emit("updated-python", this.pythonQuestions)
        })
        this.emitter.on("quiz-created_successfully", (message) => {
            this.pythonQuestions = [
                {
                    question: "",
                    sample_code: "",
                    correct_answer: "",
                    numbers: null,
                    test_case: [
                        {
                            text: "",
                            correct_answer: "",
                            numbers: null,
                        }
                    ]
                }
            ]
        })
    }
}
</script>

<style scoped>

</style>
