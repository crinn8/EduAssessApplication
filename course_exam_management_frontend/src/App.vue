<template>
    <v-app>
        <router-view/>
    </v-app>

</template>

<style lang="scss">

</style>
<script>
import store from "@/store";

export default {
    mounted() {
        if (localStorage.getItem('auth-token') !== null) {
            // store.dispatch("getMe")
        }

    }
}
</script>
