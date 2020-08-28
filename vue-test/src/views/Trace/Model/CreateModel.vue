<template>
  <div>
    <el-progress :percentage="msg" style="margin-top: 25%"></el-progress>
  </div>
</template>

<script>
export default {
  name: 'CreateModel.vue',
  data() {
    return {
      msg: 0
    }
  },
  methods: {
    prog() {
      var T = setInterval(() => {
        this.msg += Math.floor(Math.random() * 10 + 1)
        if (this.msg >= 100) {
          this.msg = 100
          clearInterval(T)
        }
      }, 100)
    }
  },
  mounted() {
    this.prog()
  }
}
</script>

<style scoped>
.el-progress {
  text-align: center;
}
</style>
