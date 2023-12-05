<template>
    <v-container>
        <h2 class="mb-3">Courses</h2>
        <v-data-table
                v-model:items-per-page="itemsPerPage"
                :headers="headers"
                :items="courses"
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
    </v-container>
</template>

<script>
import CreateCourses from "@/components/CreateCourses.vue";
import AddGrades from "@/components/AddGrades.vue";
import {VDataTable} from "vuetify/lib/labs/VDataTable";
import {api} from "@/utils/axios";
import router from "@/router";
import course from "@/views/Course.vue";

export default {
    name: "CourseList",
    components: {VDataTable, AddGrades, CreateCourses},
    data() {
        return {
            itemsPerPage: 10,
            courses: [],
            createCourseDialog: false,
            isEditCourse: false,
            selectedEditCourse: {},
            headers: [
                {
                    title: 'Name',
                    align: 'start',
                    sortable: false,
                    key: 'name',
                },

                {title: 'Actions', key: 'actions', sortable: false},
            ],
        }
    },
    methods: {
        getCourses() {
            api.get('/courses/').then(response => {
                this.courses = response.data
            })
        },
        studentDetail(student) {
            router.push({name: 'course_student_list', params: {id: student.id}})

        },
        deleteCourse(course) {
            api.delete('/courses/' + course.id + "/").then(response => {
                this.getCourses()
            })
        },
    },
    mounted() {
        this.getCourses()
    },
}
</script>

<style scoped>

</style>
