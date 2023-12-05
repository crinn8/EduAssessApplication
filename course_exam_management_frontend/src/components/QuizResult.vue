<template>
    <v-card class="mx-2">
        <v-card-title class="headline font-weight-bold text-uppercase">Quiz Results</v-card-title>
        <v-row class="ma-2" v-if="quizResults.length!==0">
            <h4>Course Average Marks :{{ quizResults[0].course_average_marks_of_students.total_numbers__avg }}</h4>
        </v-row>
        <v-row class="ma-2">
            <v-col cols="4" v-for="quiz in quizResults">
                <v-card>
                    <v-container>
                        <h5>{{ quiz.quiz_detail.name }}</h5>
                        <p>Total Number : {{ quiz.total_numbers }}</p>
                    </v-container>
                </v-card>
            </v-col>
        </v-row>
    </v-card>
</template>

<script>
export default {
    name: "QuizResult",
    props: ["quizResults"]
}
</script>

<style scoped>

</style>
