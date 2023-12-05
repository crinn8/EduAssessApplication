<template>
    <div class="chat-layout">
        <Chat />
    </div>
</template>

<script>
import Chat from "@/views/Chat.vue";

export default {
    name: "ChatLayout",
    components: {
        Chat,
    },
};
</script>

<style>
.chat-layout {
    width: 100vw;
    /* Set the layout width to the viewport width */
    height: 100vh;
    /* Set the layout height to the viewport height */
    /* Add any other desired styles for the layout */
}
</style>

