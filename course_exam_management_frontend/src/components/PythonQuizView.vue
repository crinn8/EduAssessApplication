<template>
    <v-row>
        <v-col cols="4">
            <v-row v-for="problem in pythonProblem">
                <v-col cols="12">
                    <v-card>
                        <v-container>
                            <p>{{ problem.question }}</p>
                            <v-btn @click="selectedQuiz=problem">
                                Solve
                            </v-btn>
                        </v-container>
                    </v-card>
                </v-col>
            </v-row>
        </v-col>
        <v-col cols="8">
            <PythonCompiler v-if="Object.keys(selectedQuiz).length!==0" :selectedQuiz="selectedQuiz"/>
        </v-col>
    </v-row>

</template>

<script>
import {PyStatus} from "vuepython"
import {usePython} from "usepython";

import {PyCodeBlock} from "vuepython";
import Form from "@/utils/form";
import PythonCompiler from "@/components/PythonCompiler.vue";

export default {
    name: "PythonQuizView",
    props: ["pythonProblem"],
    components: {PythonCompiler, PyStatus, PyCodeBlock},
    data() {
        return {
            py: usePython(),
            form: new Form({
                code: '',
            }),
            error: null,
            code_output: null,
            selectedQuiz: {}
        }
    },
    methods: {
        compilePythonCode() {
            this.error = null
            this.code_output = null
            this.form.submit('post', '/compile_python/').then(response => {
                console.log(response)
                this.code_output = response.output
            }).catch(error => {
                console.log(error)
                this.error = error.data.error
            })
        },
        solveQuiz() {

        }
    },
    mounted() {
        // this.py.load();
    }
}
</script>

<style scoped>

</style>
