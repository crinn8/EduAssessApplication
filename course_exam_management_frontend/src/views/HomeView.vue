<template>

    <Sidebar/>
    <v-main>
        <router-view></router-view>
    </v-main>

</template>

<script>
// @ is an alias to /src

import AppBar from "@/components/AppBar.vue";
import Sidebar from "@/components/Sidebar.vue";

export default {
    name: 'HomeView',
    components: {
        Sidebar, AppBar,
    }
}
</script>
