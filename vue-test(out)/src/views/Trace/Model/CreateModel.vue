<template>
  <div>
    <el-progress :percentage="percent" style="margin-top: 25%" v-show="showProgress"></el-progress>
    <el-dialog title="提示" :visible.sync="showDialog" width="30%">
      <span>模型构建成功，是否立即查看</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showDialog = false">取 消</el-button>
        <el-button type="primary" @click="gotolink">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CreateModel.vue',
  data() {
    return {
      percent: 0,
      showDialog: false,
      showProgress: true
    }
  },
  methods: {
    prog() {
      var T = setInterval(() => {
        var temp = 0
        temp += Math.floor(Math.random() * 10 + 1)
        this.percent += Math.floor(Math.random() * 10 + 1)
        if (this.percent >= 100) {
          this.percent = 100
          this.showProgress = false
          this.showDialog = true
          clearInterval(T)
        }
      }, 100)
    },
    gotolink() {
      this.showDialog = false
      this.$router.replace('/showModel')
    }
  },
  mounted() {
    this.prog()
  },
  created() {
    this.$http
      .get('http://127.0.0.1:8000/api/modeling')
      .then(response => {
        console.log(response)
      })
      .catch(function(error) {
        console.log(error)
      })
  }
}
</script>

<style scoped>
.el-progress {
  text-align: center;
}
</style>
