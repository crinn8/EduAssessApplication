<template>
    <v-container>
        <div v-if="showStudentCourses">
            <h2 class="mb-3">Course Students</h2>
            <v-data-table
                    v-model:items-per-page="itemsPerPage"
                    :headers="headers"
                    :items="students"
                    item-value="name"
                    class="elevation-1"
            >

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
        </div>
        <router-view></router-view>
    </v-container>
</template>

<script>
import {VDataTable} from "vuetify/lib/labs/VDataTable";
import {api} from "@/utils/axios";
import router from "@/router";
import course from "@/views/Course.vue";

export default {
    name: "CourseStudentsList",
    components: {VDataTable},
    data() {
        return {
            itemsPerPage: 10,
            students: [],
            showStudentCourses: true,
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
        getStudents() {
            api.get('/users/?classes__courses__id=' + this.$route.params.id).then(response => {
                console.log(response)
                this.students = response.data
            })
        },
        studentDetail(student) {
            this.showStudentCourses = false
            router.push({name: 'student_grades', params: {student_id: student.id}})

        },

    },
    mounted() {
        this.showStudentCourses = true
        this.getStudents()
    },
}
</script>

<style scoped>

</style>
