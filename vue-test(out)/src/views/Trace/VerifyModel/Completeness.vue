<template>
  <div id="app">
    <el-progress type="circle" :percentage="percentage" :color="colors" v-if="showProgress"></el-progress>
    <el-progress type="circle" :percentage="100" status="success" v-if="showSuccess"></el-progress>
    <el-progress type="circle" :percentage="70" status="warning" v-if="showWarning"></el-progress>
    <el-progress type="circle" :percentage="100" status="exception" v-if="showException"></el-progress>
    <el-button type="primary" @click="changeStatus" v-if="showButton" style="margin-left: 40%;margin-top: 25%;">完整性检验</el-button>
    <el-dialog :visible.sync="showDialog" title="添加场景">
      <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic" style="margin-top: 30px">
        <el-form-item v-for="(domain, index) in dynamicValidateForm.domains" :label="'场景' + index" :key="domain.key" :prop="'domains.' + index + '.value'">
          <el-input v-model="domain.value" style="width: 400px"></el-input>
          <el-button @click.prevent="removeDomain(domain)" style="margin-left: 10px">删除</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>
          <el-button @click="addDomain">新增场景</el-button>
          <el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <el-dialog title="提示" :visible.sync="dialogVisible" width="30%" :before-close="handleClose">
      <span>检测到场景xxx缺失，是否添加此场景</span>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="cycle">Yes! 添加该场景</el-button>
        <el-button
          @click="
            dialogVisible = false
            showDialog = true
          "
          >No! 手动添加场景</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'EditModel.vue',
  data() {
    return {
      percentage: 0,
      showButton: true,
      showProgress: false,
      showSuccess: false,
      showWarning: false,
      showException: false,
      showDialog: false,
      dialogVisible: false,
      showSpan: false,
      colors: [
        { color: '#CCCCCC', percentage: 20 },
        { color: '#CCCC99', percentage: 40 },
        { color: '#1989fa', percentage: 60 },
        { color: '#e6a23c', percentage: 80 },
        { color: '#17CD6C', percentage: 100 }
      ],
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      },
      dynamicValidateForm: {
        domains: [
          {
            value: ''
          }
        ],
        email: ''
      },
      formLabelWidth: '120px'
    }
  },
  methods: {
    changeStatus() {
      this.showButton = false
      this.percentage = 0
      this.showProgress = !this.showProgress
      this.showSpan = true
      this.showSuccess = false
      this.showWarning = false
      this.showException = false
    },
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('submit!')
        } else {
          console.log('error submit!!')
          return false
        }
      })
      this.showDialog = false
      this.showButton = true
      this.showProgress = false
      this.showSuccess = false
      this.showWarning = false
      this.showException = false
      this.showSpan = false
    },
    cycle() {
      this.showDialog = false
      this.showButton = true
      this.showProgress = false
      this.showSuccess = false
      this.showWarning = false
      this.showException = false
      this.dialogVisible = false
      this.showSpan = false
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    removeDomain(item) {
      var index = this.dynamicValidateForm.domains.indexOf(item)
      if (index !== -1) {
        this.dynamicValidateForm.domains.splice(index, 1)
      }
    },
    addDomain() {
      this.dynamicValidateForm.domains.push({
        value: '',
        key: Date.now()
      })
    },
    prog() {
      var T = setInterval(() => {
        this.percentage += Math.floor(Math.random() * 10 + 1)
        if (this.percentage >= 100) {
          this.percentage = 100
          clearInterval(T)
          this.changeStatus()
        }
      }, 100)
    }
  },
  mounted() {
    this.prog()
    // let _this = this // 声明一个变量指向Vue实例this，保证作用域一致
    // this.timer = setInterval(() => {
    //   if (_this.percentage < 100) _this.percentage += Math.floor(Math.random() * 10 + 1) //取得介于 1 到 10 之间的一个随机数
    //   if (this.percentage >= 100) {
    //     // clearInterval(this.timer) // 在Vue实例销毁前，清除我们的定时器
    //     _this.percentage = -10000
    //     this.showProgress = false
    //     this.showException = true
    //     this.showButton = false
    //     this.dialogVisible = true
    //   }
    // }, 300)
  }
}
</script>

<style scoped>
.el-progress {
  margin-left: 40%;
  margin-top: 10%;
  /*width: 300px;*/
}
</style>
