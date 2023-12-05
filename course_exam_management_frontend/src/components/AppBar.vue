<template>

    <v-app-bar color="#dc899e" class="flex-grow-0" app dark>
        <template v-slot:append>
            <!-- <v-btn icon="mdi-face-man-profile" @click="$refs.profile.click()"></v-btn> -->
            <v-btn icon="mdi-lock-reset" href="change-password"></v-btn>
            <v-btn icon="mdi-logout" @click="logout"></v-btn>

            <v-file-input @change="imageUploaded" ref="profile" style="display: none" accept="image/jpeg, image/png"></v-file-input>

    <v-dialog v-model="showDialog" persistent max-width="350">
      <v-card>
        <v-card-title class="headline">Logout Confirmation</v-card-title>
        <v-card-text>Are you sure you want to log out?</v-card-text>
        <v-card-actions>
          <v-btn text @click="showDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmLogout">Logout</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

        </template>

    </v-app-bar>


</template>

<script>
import {mapGetters} from "vuex";
import {api} from "@/utils/axios";
import store from "@/store";

export default {
    name: "AppBar",

    data: () => ({
        drawer: false,
        showDialog: false
    }),
    computed: {
        ...mapGetters([
            'fetchMe',
        ])

    },

    methods: {
        logout() {
            this.showDialog = true;
        },
        confirmLogout() {
            localStorage.removeItem('auth-token');
            localStorage.removeItem('vuex');
            this.$router.push('/login');
        },

        imageUploaded(e) {
            console.log("!!!!")
            console.log(this.fetchMe.id)
            let formData = {};
            formData['image'] = e.target.files[0];
            api.patch('/users/' + this.fetchMe.id + "/", formData, {headers: {'Content-Type': 'multipart/form-data'}}).then(response => {
                store.dispatch("getMe")
            }).catch(error => {
                console.log(error)
            })
        },
    }
}
</script>

<style scoped>

</style>
