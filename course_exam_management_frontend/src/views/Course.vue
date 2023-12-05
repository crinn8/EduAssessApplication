<template>
    <StudentCourses v-if="fetchMe.is_student"/>
    <TeacherCourses v-else/>
</template>

<script>
import TeacherCourses from "@/components/TeacherCourses.vue";
import {mapGetters} from "vuex";
import StudentCourses from "@/components/StudentCourses.vue";

export default {
    name: "Course",
    components: {StudentCourses, TeacherCourses},
    computed: {
        ...mapGetters([
            'fetchMe',
        ])

    },
    mounted() {
        console.log(this.fetchMe.is_superuser)
        // if (this.fetchMe.is_superuser === undefined) {
        //     window.location.reload()
        // }
        if (this.fetchMe.is_superuser) {
            this.$router.push('/users')
        }
    }
}
</script>

<style scoped>

</style>
