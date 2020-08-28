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
    <el-dialog name="failure" title="提示" :visible.sync="showFailureDialog" width="30%">
      <span>{{ outMessage }}</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="gotolink">Yes! 立即添加</el-button>
        <el-button @click="refresh">No，稍后添加</el-button>
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
      outMessage: '模型不完整，是否立即补全',
      res: '',
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
        this.percentage += Math.floor(Math.random() * 50 + 10)
        if (this.percentage >= 100) {
          this.percentage = 100
          if (this.isButton == true) {
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
        .get('http://127.0.0.1:8000/api/judgeModel')
        .then(response => {
          console.log(response)
          this.res = response.data.result
          if (this.res == 'Y') {
            //todo 跳出检测成功的弹窗
            // this.showButton = true
            this.showSuccessDialog = true
            // this.showFailureDialog = true
          } else if (this.res == 'N') {
            //todo 跳出检测失败的弹窗
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
