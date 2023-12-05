<template>
    <v-container>
        <h2 class="mb-3">Classes</h2>
        <v-data-table
                v-model:items-per-page="itemsPerPage"
                :headers="headers"
                :items="classes"
                item-value="name"
                class="elevation-1"
        >

            <template v-slot:top>
                <v-toolbar
                        flat
                >
                    <v-toolbar-title>Classes</v-toolbar-title>

                    <v-spacer></v-spacer>
                    <v-btn
                            color="primary"
                            class="mb-2 justify-end"
                            @click="openClassForm"
                    >
                        New Class
                    </v-btn>


                </v-toolbar>
                <CreateClass :create-class-dialog="createClassDialogValue"
                             @update-create-class-dialog-value="updateClassDialogValue"/>
            </template>
            <template v-slot:item.actions="{ item }">
                <v-icon
                        size="small"
                        class="me-2"
                        @click="editClass(item.raw)"
                >
                    mdi-pencil
                </v-icon>
                <v-icon
                        size="small"
                        @click="deleteClass(item.raw)"
                >
                    mdi-delete
                </v-icon>
            </template>
        </v-data-table>
    </v-container>
    <delete-model/>
</template>

<script>
import CreateClass from "@/components/CreateClass.vue";
import {api} from "@/utils/axios";
import router from "@/router";
import {VDataTable} from "vuetify/lib/labs/VDataTable";
import CreateQuiz from "@/components/CreateQuiz.vue";
import DeleteModel from "@/components/common/DeleteModel.vue";

export default {
    name: "ClassList",
    components: {DeleteModel, CreateQuiz, VDataTable, CreateClass},
    data() {
        return {
            itemsPerPage: 10,
            classes: [],
            createClassDialogValue: false,
            headers: [
                {
                    title: 'Title',
                    align: 'start',
                    sortable: false,
                    key: 'name',
                },
                {title: 'Created At', align: 'start', key: 'created_at'},
                {title: 'Actions', key: 'actions', sortable: false},
            ],
        }
    },
    methods: {
        getClass() {
            api.get('/classes/').then(response => {
                this.classes = response.data
            })
        },
        updateClassDialogValue(value) {
            this.createClassDialogValue = value
            this.getClass()
        },
        openClassForm() {
            this.createClassDialogValue = true
        },
        editClass(classObj) {
            this.createClassDialogValue = true
            this.emitter.emit("edit-class", classObj)

        },
        deleteClass(obj) {
            this.emitter.emit("delete-record", '/classes/' + obj.id + "/")
        },

    },

    mounted() {
        this.getClass()
    },
    created() {
        this.emitter.on("record-deleted", () => {
            this.getClass()
        })
    }
}
</script>

<style scoped>

</style>
