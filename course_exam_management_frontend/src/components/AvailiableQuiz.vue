<template>
    <v-card class="mx-2">
        <v-card-title class="headline font-weight-bold text-uppercase">Quizzes</v-card-title>
        <v-row class="ma-2">
            <v-col cols="4" v-for="quiz in quizes">
                <v-card>
                    <v-container>
                        <p>{{ quiz.name }}</p>
                        <v-btn @click="quizSelected(quiz)">
                            Solve
                        </v-btn>
                    </v-container>
                </v-card>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    name: "AvailiableQuiz",
    props: ["quizes"],
    methods: {
        quizSelected(quiz) {
            this.emitter.emit("quiz-selected", quiz)
        }
    }
}
</script>

<style scoped>

</style>
