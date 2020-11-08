<template>
  <div>
    <el-progress type="circle" :percentage="percentage" :color="colors" v-show="showProgress"></el-progress>
    <el-button type="primary" v-show="showButton" @click="buttonClick" style="margin-left: 40%;margin-top: 25%;">完整性检验</el-button>
    <!--    <h1>{{ res }}</h1>-->
    <el-dialog name="success" title="提示" :visible.sync="showSuccessDialog" width="30%">
      <span>模型完整</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="this.refresh">确认</el-button>
        <!--        <el-button>退出</el-button>-->
      </span>
    </el-dialog>
    <el-dialog name="failure" title="模型不完整，请补全" :visible.sync="showFailureDialog" width="60%">
      <span style="white-space: pre-line">{{ msg }}</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="gotolink">Yes！立即补全</el-button>
        <el-button @click="refresh">No，稍后补全</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'JudgeModel.vue',
  inject: ['reload'],
  data() {
    return {
      percentage: 0,
      showButton: true,
      showProgress: false,
      isButton: false,
      showSuccessDialog: false,
      showFailureDialog: false,
      res: '',
      msg: '',
      colors: [
        { color: '#CCCCCC', percentage: 20 },
        { color: '#CCCC99', percentage: 40 },
        { color: '#1989fa', percentage: 60 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#17CD6C', percentage: 100 }
      ]
    }
  },
  methods: {
    buttonClick() {
      this.showButton = false
      this.showProgress = true
      this.isButton = true
      this.percentage = 0
    },
    prog() {
      var T = setInterval(() => {
        this.percentage += Math.floor(Math.random() * 5 + 10)
        if (this.percentage >= 100) {
          this.percentage = 100
          if (this.isButton === true) {
            this.dialogVisible = true
            this.showProgress = false
            this.judgeResult()
            clearInterval(T)
          }
        }
      }, 100)
    },
    judgeResult() {
      this.$http
        .get('http://127.0.0.1:8000/api/judge_model')
        .then(response => {
          console.log(response)
          this.res = response.data.result
          this.msg = response.data.msg
          // console.log(this.msg)
          if (this.res === 'Y') {
            // this.showButton = true
            this.showSuccessDialog = true

            // this.showFailureDialog = true
          } else if (this.res === 'N') {
            // this.showProgress = true
            this.showFailureDialog = true
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    gotolink() {
      this.$router.replace('/CompletionModel')
    },
    refresh() {
      this.showFailureDialog = false
      this.reload()
    }
  },
  mounted() {
    this.prog()
  }
}
</script>

<style lang="scss" scoped>
.el-progress {
  margin-left: 40%;
  margin-top: 10%;
  /*width: 300px;*/
}
</style>
