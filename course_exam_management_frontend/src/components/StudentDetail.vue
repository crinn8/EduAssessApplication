<template>
    <v-container>
        <h2 class="mb-3">Student Detail</h2>
        <v-card class="mt-2 mb-2 ml-2 mr-2">
            <v-row class="ma-2" v-if="quizes.length!==0">
                <h4>Average Marks :{{ quizes[0].student_average_marks.total_numbers__avg }}</h4>
            </v-row>
            <v-row class="ma-2" v-if="quizes.length!==0">
                <h4>Total Marks :{{ quizes[0].student_total_marks.total_numbers__sum }}</h4>
            </v-row>
            <v-dialog
                    v-model="dialog"
                    persistent
                    width="auto"
            >
                <v-card>
                    <v-card-text>
                        <h3 v-if="selectedRow.delivered_mcqs.length!==0">Multiple-choice questions answer:</h3>
                        <div v-for="data in selectedRow.delivered_mcqs" class="mt-3 ">
                            <p> {{ data.mcqs_quiz_detail.question }}</p>
                            <div v-for="i in data.solved_mcqs_answers" class="ml-3">
                                <span>{{ i.answer }}</span>
                            </div>
                        </div>

                        <h3 v-if="selectedRow.delivered_python.length!==0">Python problem answer:</h3>
                        <div v-for="data in selectedRow.delivered_python" class="mt-3 ">
                            <p>{{ data.python_quiz_detail.question }}</p>

                            <p class="ml-3" v-for="output in data.code.split('\n')">{{ output }}</p>

                        </div>

                    </v-card-text>
                    <v-card-actions>
                        <v-btn color="primary" block @click="dialog = false">Close</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
            <v-data-table
                    v-model:items-per-page="itemsPerPage"
                    :headers="headers"
                    :items="quizes"
                    item-value="name"
                    class="elevation-1"
            >

                <template v-slot:top>
                    <v-toolbar
                            flat
                    >
                        <v-toolbar-title>Grade's</v-toolbar-title>

                        <!--                    <v-spacer></v-spacer>-->
                        <v-btn
                                color="#dc899e"
                                class="mb-2 justify-end"
                                @click="createGradeDialogValue = true"
                        >
                            Add Grade
                        </v-btn>

                    </v-toolbar>
                    <AddGrades :create-grade-dialog="createGradeDialogValue"
                               @update-create-grade-dialog-value="updateGradeDialogValue"/>
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon
                            size="small"
                            class="me-2"
                            @click="editQuiz(item.raw)"
                    >
                        mdi-pencil
                    </v-icon>
                    <v-icon
                            size="small"
                            class="me-2"
                            @click="detail(item.raw)"
                    >
                        mdi-eye
                    </v-icon>
                </template>
            </v-data-table>
        </v-card>
    </v-container>
</template>

<script>
import {VDataTable} from 'vuetify/labs/VDataTable'
import {api} from "@/utils/axios";
import CreateQuiz from "@/components/CreateQuiz.vue";
import AddGrades from "@/components/AddGrades.vue";

export default {
    name: "QuizList",
    components: {
        CreateQuiz,
        VDataTable,
        AddGrades
    },
    data() {
        return {
            itemsPerPage: 10,
            createGradeDialogValue: false,
            quizes: [],
            dialog: false,
            selectedRow: {},
            headers: [
                {
                    title: 'Quiz',
                    align: 'start',
                    sortable: false,
                    key: 'quiz_detail.name',
                },
                {
                    title: 'Student',
                    align: 'start',
                    sortable: false,
                    key: 'students_detail.username',
                },
                {
                    title: 'Course',
                    align: 'start',
                    sortable: false,
                    key: 'course_detail.name',
                },
                {title: 'Total Numbers', align: 'start', key: 'total_numbers'},
                {title: 'Actions', key: 'actions', sortable: false},
            ],
        }
    },
    methods: {
        getQuizes() {
            api.get('/delivered_quiz/?student__id=' + this.$route.params.student_id).then(response => {
                this.quizes = response.data
            })
        },
        updateGradeDialogValue(value) {
            this.createGradeDialogValue = value
            this.getQuizes()
        },
        editQuiz(quizObj) {
            this.createGradeDialogValue = true
            this.emitter.emit("edit-grade", quizObj)

        },
        detail(quizObj) {
            this.dialog = true
            this.selectedRow = quizObj
            console.log(this.selectedRow)

        },

    },
    mounted() {
        this.getQuizes()
    },
}
</script>

<style scoped>

</style>
