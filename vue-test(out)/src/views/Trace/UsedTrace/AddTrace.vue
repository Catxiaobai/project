<template>
  <div>
    <el-form :model="addForm" :rules="rules" ref="addForm">
      <el-form-item label="场景名称" label-width="120px" prop="name">
        <el-input v-model="addForm.name" clearable placeholder="请输入场景名称"></el-input>
      </el-form-item>
      <el-form-item label="场景内容" label-width="120px" prop="content">
        <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景具体内容"> </el-input>
      </el-form-item>
      <el-form-item label="场景描述" label-width="120px" prop="details">
        <el-input v-model="addForm.details" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景文字描述"> </el-input>
      </el-form-item>
      <el-form-item label="场景介绍" label-width="120px" prop="describe">
        <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景简单介绍"> </el-input>
      </el-form-item>
    </el-form>

    <el-button @click="dialogAddTrace = false" style="margin-left: 40%;width: 100px">取 消</el-button>
    <el-button type="primary" @click="handleAddCommit('addForm')" style="margin-left: 50px;width: 100px">确 定</el-button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogAddTrace: false, //添加trace弹窗
      addForm: {
        //添加时使用
        name: '',
        content: '',
        details: '',
        describe: ''
      },
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        content: [{ required: true, message: '不能为空', trigger: 'blur' }],
        details: [{ required: true, message: '不能为空', trigger: 'blur' }],
        describe: [{ required: true, message: '不能为空', trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleAddCommit(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // alert('submit!')
          this.dialogAddTrace = false
          console.log(this.addForm)
          this.$http
            .post('http://127.0.0.1:8000/api/add_trace', this.addForm)
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                // this.pageList()
                console.log('success')
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped></style>
