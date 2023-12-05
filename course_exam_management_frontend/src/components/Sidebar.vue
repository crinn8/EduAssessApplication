<template>

    <v-navigation-drawer
            v-model="drawer"
            :rail="rail"
            permanent
            @click="rail = false"
    >
        <v-list-item
                :prepend-avatar="extractDirectUrl(fetchMe.image)"
                :title="fetchMe.username"
                nav
        >
            <template v-slot:append>
                <v-btn
                        variant="text"
                        icon="mdi-chevron-left"
                        @click.stop="rail = !rail"
                ></v-btn>
            </template>
        </v-list-item>

        <v-divider></v-divider>

        <v-list density="compact" nav>
            <router-link to="/" v-if="!fetchMe.is_superuser">
                <v-list-item prepend-icon="mdi-cast-education" title="Courses" value="courses"></v-list-item>
            </router-link>
            <router-link to="/quiz" v-if="!fetchMe.is_student && !fetchMe.is_superuser">
                <v-list-item prepend-icon="mdi-clipboard-edit-outline" title="Quizzes" value="quiz">
                </v-list-item>
            </router-link>
            <router-link to="/classes" v-if="!fetchMe.is_student && !fetchMe.is_superuser">
                <v-list-item prepend-icon="mdi-book-variant" title="Classes" value="classes">
                </v-list-item>
            </router-link>
            <router-link to="/grades" v-if="!fetchMe.is_student && !fetchMe.is_superuser">
                <v-list-item prepend-icon="mdi-school" title="Grades" value="grades">
                </v-list-item>
            </router-link>
                <router-link to="/chat" v-if="!fetchMe.is_student && !fetchMe.is_superuser">
          <v-list-item prepend-icon="mdi-chat" title="ChatGPT" value="chat"></v-list-item>
        </router-link>
            <router-link to="/users" v-if="fetchMe.is_superuser">
                <v-list-item prepend-icon="mdi-cast-education" title="Users" value="users"></v-list-item>
            </router-link>
        </v-list>
    </v-navigation-drawer>

    <AppBar/>


</template>

<script>
import AppBar from "@/components/AppBar.vue";
import {mapGetters} from "vuex";
import router from "@/router";

export default {
    name: "Sidebar",
    components: {AppBar},
    data() {
        return {
            drawer: true,
            items: [
                {title: 'Home', icon: 'mdi-home-city'},
                {title: 'My Account', icon: 'mdi-account'},
                {title: 'Users', icon: 'mdi-account-group-outline'},
            ],
            rail: false,
        }
    },
    computed: {
        ...mapGetters([
            'fetchMe',
        ])
    },
    mounted() {
        if (this.fetchMe.is_superuser) {
            router.push({name: 'users'})
        }
    },
    methods: {
        extractDirectUrl(signedUrl) {
            // console.log("!!!!"+signedUrl)
            let modifiedUrl = signedUrl.replace('http://127.0.0.1:8000/media/', '');
            // console.log(modifiedUrl);
            return modifiedUrl;
        }
    }
}
</script>

<style scoped>

</style>
