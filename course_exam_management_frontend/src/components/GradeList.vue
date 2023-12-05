<template>
    <v-container>
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
                    <v-toolbar-title>Students</v-toolbar-title>

                </v-toolbar>
                <AddGrades :create-grade-dialog="createGradeDialogValue"
                           @update-create-grade-dialog-value="updateGradeDialogValue"/>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon
                        size="small"
                        class="me-2"
                        @click="studentDetail(item.raw)"
                >
                    mdi-eye-circle-outline
                </v-icon>
            </template>
        </v-data-table>
    </v-container>
</template>

<script>
import {VDataTable} from 'vuetify/labs/VDataTable'
import {api} from "@/utils/axios";
import CreateQuiz from "@/components/CreateQuiz.vue";
import AddGrades from "@/components/AddGrades.vue";
import router from "@/router";

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
            headers: [
                {
                    title: 'Email',
                    align: 'start',
                    sortable: false,
                    key: 'email',
                },

                {title: 'Actions', key: 'actions', sortable: false},
            ],
        }
    },
    methods: {
        getQuizes() {
            api.get('/users/?is_student=true').then(response => {
                this.quizes = response.data
            })
        },
        updateGradeDialogValue(value) {
            this.createGradeDialogValue = value
            this.getQuizes()
        },
        studentDetail(student) {
            router.push({name: 'student_detail', params: {id: student.id}})

        },

    },
    mounted() {
        this.getQuizes()
    },
}
</script>

<style scoped>

</style>
