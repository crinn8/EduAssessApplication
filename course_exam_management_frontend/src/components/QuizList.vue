<template>
    <v-container>
        <h2 class="mb-3">Quiz's</h2>
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
                    <v-toolbar-title>Quizzes</v-toolbar-title>

                    <v-btn
                            color="primary"
                            class="mb-2 justify-end"
                            @click="createQuizDialogValue = true"
                    >
                        New Quiz
                    </v-btn>

                </v-toolbar>
                <CreateQuiz :create-quiz-dialog="createQuizDialogValue"
                            @update-create-quiz-dialog-value="updateQuizDialogValue"/>
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
                        @click="deleteQuiz(item.raw)"
                >
                    mdi-delete
                </v-icon>
            </template>
        </v-data-table>
    </v-container>
    <delete-model/>
</template>

<script>
import {VDataTable} from 'vuetify/labs/VDataTable'
import {api} from "@/utils/axios";
import CreateQuiz from "@/components/CreateQuiz.vue";
import DeleteModel from "@/components/common/DeleteModel.vue";

export default {
    name: "QuizList",
    components: {
        DeleteModel,
        CreateQuiz,
        VDataTable,
    },
    data() {
        return {
            itemsPerPage: 10,
            createQuizDialogValue: false,
            quizes: [],
            headers: [
                {
                    title: 'Title',
                    align: 'start',
                    sortable: false,
                    key: 'name',
                },
                {title: 'Description', align: 'start', key: 'description'},
                {title: 'Created At', align: 'start', key: 'created_at'},
                {title: 'Actions', key: 'actions', sortable: false},
            ],
        }
    },
    methods: {
        getQuizes() {
            api.get('/quizes/').then(response => {
                this.quizes = response.data
            })
        },
        updateQuizDialogValue(value) {
            this.createQuizDialogValue = value
            this.getQuizes()
        },
        editQuiz(quizObj) {
            this.createQuizDialogValue = true
            this.emitter.emit("edit-quiz", quizObj)

        },
        deleteQuiz(obj) {
            this.emitter.emit("delete-record", '/quizes/' + obj.id + "/")
            // api.delete('/quizes/' + obj.id + "/").then(response => {
            //     this.getQuizes()
            // })
        },
    },
    mounted() {
        this.getQuizes()
    },
    created() {
        this.emitter.on("record-deleted", () => {
            this.getQuizes()
        })
    }
}
</script>

<style scoped>

</style>
