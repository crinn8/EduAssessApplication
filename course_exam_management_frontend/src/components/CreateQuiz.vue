<template>
    <v-row justify="end" class="mt-2 mr-1 mb-2">
        <v-dialog
                v-model="createQuizDialogCompute"
                fullscreen
                :scrim="false"
                transition="dialog-bottom-transition"
        >

            <v-card>
                <v-toolbar
                        dark
                        color="#dc899e"
                >
                    <v-btn
                            icon
                            dark
                            @click="createQuizDialogCompute=false"
                    >
                        <v-icon>mdi-close</v-icon>
                    </v-btn>
                            <v-toolbar-title v-if="!isQuizEdit">Create Quiz</v-toolbar-title>
                            <v-toolbar-title v-else>Edit Quiz</v-toolbar-title>
                            <v-spacer></v-spacer>
                    </v-toolbar>

                         <v-col > 
                                <h2>🤖️ If you need help, you can use the EduAssess AI:</h2></v-col>
                          <v-col>
                            <v-textarea 
                                rows="8"
                                v-model="res"
                                density="compact"
                                readonly="true"
                                :style="{ width: '1200px', 'margin-left': '150px' }"
                            ></v-textarea> 
                                <div class="chat" style="margin-top: -10px;">
                                    <input class="input" placeholder="Ask me about..." v-model="content" clear> <br>
                                    <div class="btnc" style="margin-top: 10px;"><button class="btn" @click="askAi">{{ btnText }}</button></div>

                                </div>
                            </v-col> 

                <v-form @submit.prevent="createQuiz">
                    <v-container>
                        <h3>Quiz Information</h3>
                        <v-row>
                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.name"
                                        label="Title"
                                        :rules="rules"
                                ></v-text-field>
                            </v-col>

                            <v-col
                                    cols="6"
                            >
                                <v-text-field
                                        v-model="form.description"
                                        label="Description"
                                        :rules="rules"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                        <CreateMCQSPaper :form="form" :updated-quizmcqs="updatedQuizmcqs"/>
                        <v-divider :thickness="7" class="border-opacity-100 mt-3 mb-3"></v-divider>
                        <CreatePythonPaper :updatedQuizpython="updatedQuizpython"/>
                      
                        <v-alert v-model="formValid" color="error" class="mt-3 mb-3"
                                 text="Please fill the form Properly."></v-alert>

                        <v-alert v-model="formValid" color="info"
                                 text="Please make sure that Every question has at least one option is required"></v-alert>

                        <v-row justify="center">
                            <v-col cols="6">
                                <v-btn type="submit" color="#dc899e" block class="mt-2" v-if="!isQuizEdit">Create Quiz
                                </v-btn>
                                <v-btn @click="updateQuiz" color="#dc899e" block class="mt-2" v-else>Update Quiz</v-btn>
                            </v-col>
                        </v-row>
                    </v-container>

                </v-form>

            </v-card>


        </v-dialog>
    </v-row>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios'

console.log(import.meta.env)
const http = axios.create({
    baseURL: 'https://api.openai.com/v1/chat',
    headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer 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`,
    }
});
const content = ref('');
const BTN_TEXT = 'Ask 🚀'
const res = ref('The answer will be displayed here.')
const btnText = ref(BTN_TEXT)
const askAi = () => {
    btnText.value = 'Thinking...🤔'
    http.post('/completions', {
        "model": "gpt-3.5-turbo",
        "messages": [{ "role": "user", "content": content.value }],
        "temperature": 0.7
    }).then(function (response) {
        console.log(response);
        res.value = response.data.choices[0].message.content
    }).catch(function (error) {
        console.log(error);
    }).finally(() => {
        btnText.value = BTN_TEXT
    })
}
</script>

<script>
import Form from "@/utils/form";
import {api} from "@/utils/axios";
import router from "@/router";
import store from "@/store";
import {mapGetters} from "vuex";
import {formToJSON} from "axios";
import CreateMCQSPaper from "@/components/CreateMCQSPaper.vue";
import {eventBus} from "@/utils/eventBus";
import CreatePythonPaper from "@/components/CreatePythonPaper.vue";

export default {
    name: "CreateQuiz",
    props: [
        "createQuizDialog"
    ],
    components: {CreatePythonPaper, CreateMCQSPaper},
    data() {
        return {
            name: null,
            description: null,
            createQuizDialogValue: false,
            quizEditId: null,
            isQuizEdit: false,
            updatedQuizmcqs: [],
            updatedQuizpython: [],
            form: new Form({
                name: null,
                description: null,
                quizmcqs: [],
                quizpython: [],
            }),
            formValid: false,
            rules: [
                value => {
                    if (value) return true

                    return 'This Field Cannot be blank'
                },
            ],


        }
    },
    methods: {
        getUsers() {
            api.get('/users/?is_student=true').then(response => {
                this.users = response.data
            })
        },

        createQuiz() {
            this.formValid = false
            this.emitter.emit("send-quiz-data", true)

            this.form.submit('post', '/quizes/').then(response => {
                this.$emit("update-courses")
                this.createQuizDialogValue = false
                this.emitter.emit("quiz-created_successfully")
                this.$emit('update-create-quiz-dialog-value', false)

            }).catch(error => {
                this.formValid = true
            })
        },

        updateQuiz() {
            this.formValid = false
            this.emitter.emit("send-quiz-data", true)

            this.form.submit('patch', '/quizes/' + this.quizEditId + "/").then(response => {
                this.form.reset()
                this.form.quizmcqs = []
                this.form.quizpython = []
                this.$emit("update-courses")
                this.createQuizDialogValue = false
                this.emitter.emit("quiz-created_successfully")
                this.$emit('update-create-quiz-dialog-value', false)


            }).catch(error => {
                this.formValid = true
            })
        },


    },
    computed: {

        createQuizDialogCompute: {
            get() {
                this.createQuizDialogValue = this.createQuizDialog
                return this.createQuizDialogValue
            },
            set(value) {
                console.log(value)
                this.$emit('update-create-quiz-dialog-value', value)
            }
        }
    },
    mounted() {

    },
    created() {
        this.emitter.on("updated-mcqs", (message) => {
            this.form.quizmcqs = message
        })
        this.emitter.on("updated-python", (message) => {
            this.form.quizpython = message
        })
        this.emitter.on("edit-quiz", (classObj) => {
            // this.emitter.emit("updated-mcqs", classObj)
            this.form.name = classObj.name
            this.form.description = classObj.description
            this.form.quizmcqs = classObj.quizmcqs_set
            this.form.quizpython = classObj.quizpythonproblem_set
            this.updatedQuizmcqs = classObj.quizmcqs_set
            this.updatedQuizpython = classObj.quizpythonproblem_set
            this.quizEditId = classObj.id
            this.isQuizEdit = true


        })
    }
}
</script>

<style scoped>
.dialog-bottom-transition-enter-active,
.dialog-bottom-transition-leave-active {
    transition: transform .2s ease-in-out;
}

h1 {
    margin-bottom: 64px;
}

.input {
    width: 1200px;
    height: 32px;
    padding: 20px;
    margin-left: 150px;
    border: none;
    border-radius: 16px;
    box-shadow: 2px 2px 7px 0 rgb(0, 0, 0, 0.2);
    outline: none;
    font-size: 16px;
}

.input:invalid {
    animation: justshake 0.3s forwards;
    color: red;
}

@keyframes justshake {
    25% {
        transform: translateX(5px);
    }

    50% {
        transform: translateX(-5px);
    }

    75% {
        transform: translateX(5px);
    }

    100% {
        transform: translateX-(5px);
    }
}

/* button {
    cursor: pointer;
    height: 32px;
    font-size: 16px;
    margin-top: 24px;
    background: royalblue;
    color: white;
    padding: 0.7em 1em;
    padding-left: 0.9em;
    display: flex;
    align-items: center;
    border: none;
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.2s;
}

button span {
    display: block;
    margin-left: 0.3em;
    transition: all 0.3s ease-in-out;
}

button svg {
    display: block;
    transform-origin: center center;
    transition: transform 0.3s ease-in-out;
} */

.btnc {
    display: flex;
    flex-direction: column;
    margin-left: 650px;
}

.card {
    border-radius: 16px;
    background: white;
    position: relative;
    display: flex;
    place-content: center;
    place-items: center;
    overflow: hidden;
    border-radius: 16px;
    margin: 24px 0;
    margin-left: 150px;
    height: 200px;
    width: 1200px;
}

.card pre {
    z-index: 1;
    color: black;
    font-size: 16px;
    white-space: pre-wrap;
    /* Allows line breaks */
    word-break: break-word;
    /* Breaks words when necessary */
    text-align: center;
    /* Centers the text horizontally */
}

.card {
    margin-top: 32px;
}

.card span,

.card::before {
    border-radius: 16px;
    content: '';
    position: absolute;
    width: 100%;
    height: 130%;
    animation: rotBGimg 3s linear infinite;
    transition: all 0.2s linear;
}

.card::after {
    content: '';
    position: absolute;
    background: white;
    ;
    inset: 5px;
}

.button-block {
    display: flex;
    align-items: center;
    justify-content: end;
}

.btn {
    display: flex;
    justify-content: center;
    align-items: center;
    min-width: 8rem;
    max-width: 13rem;
    height: 3rem;
    background-size: 300% 300%;
    backdrop-filter: blur(1rem);
    border-radius: 5rem;
    transition: 0.5s;
    animation: gradient_301 5s ease infinite;
    border: double 4px transparent;
    background-image: linear-gradient(137.48deg, #ffdb3b 10%, #FE53BB 45%, #8F51EA 67%, #0044ff 87%), linear-gradient(137.48deg, #ffdb3b 10%, #FE53BB 45%, #8F51EA 67%, #0044ff 87%);
    background-origin: border-box;
    background-clip: content-box, border-box;
}

#container-stars {
    position: fixed;
    z-index: -1;
    width: 100%;
    height: 100%;
    overflow: hidden;
    transition: 0.5s;
    backdrop-filter: blur(1rem);
    border-radius: 5rem;
}

strong {
    z-index: 2;
    font-size: 16px;
    color: #FFFFFF;
    text-shadow: 0 0 4px white;
}

#glow {
    position: absolute;
    display: flex;
    width: 12rem;
}

.circle {
    width: 100%;
    height: 30px;
    filter: blur(2rem);
    animation: pulse_3011 4s infinite;
    z-index: -1;
}

.circle:nth-of-type(1) {
    background: rgba(254, 83, 186, 0.636);
}

.circle:nth-of-type(2) {
    background: rgba(142, 81, 234, 0.704);
}

.btn:hover #container-stars {
    z-index: 1;
    background-color: #212121;
}

.btn:hover {
    transform: scale(1.1)
}

.btn:active {
    border: double 4px #FE53BB;
    background-origin: border-box;
    background-clip: content-box, border-box;
    animation: none;
}

.btn:active .circle {
    background: #FE53BB;
}

#stars {
    position: relative;
    background: transparent;
    width: 200rem;
    height: 200rem;
}

#stars::after {
    content: "";
    position: absolute;
    top: -10rem;
    left: -100rem;
    width: 100%;
    height: 100%;
    animation: animStarRotate 90s linear infinite;
}

#stars::after {
    background-image: radial-gradient(#ffffff 1px, transparent 1%);
    background-size: 50px 50px;
}

#stars::before {
    content: "";
    position: absolute;
    top: 0;
    left: -50%;
    width: 170%;
    height: 500%;
    animation: animStar 60s linear infinite;
}

#stars::before {
    background-image: radial-gradient(#ffffff 1px, transparent 1%);
    background-size: 50px 50px;
    opacity: 0.5;
}

@keyframes animStar {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(-135rem);
    }
}

@keyframes animStarRotate {
    from {
        transform: rotate(360deg);
    }

    to {
        transform: rotate(0);
    }
}

@keyframes gradient_301 {
    0% {
        background-position: 0% 50%;
    }

    50% {
        background-position: 100% 50%;
    }

    100% {
        background-position: 0% 50%;
    }
}

@keyframes pulse_3011 {
    0% {
        transform: scale(0.75);
        box-shadow: 0 0 0 0 rgba(202, 88, 88, 0.7);
    }

    70% {
        transform: scale(1);
        box-shadow: 0 0 0 10px rgba(117, 35, 35, 0);
    }

    100% {
        transform: scale(0.75);
        box-shadow: 0 0 0 0 rgba(0, 0, 0, 0);
    }
}
</style>

