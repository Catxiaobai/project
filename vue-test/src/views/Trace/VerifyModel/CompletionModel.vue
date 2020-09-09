<template>
  <div>
    <el-form :model="dynamicValidateForm" ref="dynamicValidateForm" label-width="100px" class="demo-dynamic" style="margin-top: 30px">
      <el-form-item v-for="(domain, index) in dynamicValidateForm.domains" :label="'场景' + index" :key="domain.key" :prop="'domains.' + index + '.value'">
        <el-input v-model="domain.value" placeholder="请输入Trace" style="width: 80%" type="textarea" :rows="7"></el-input>
        <el-button @click.prevent="removeDomain(domain)" style="margin-left: 10px">删除</el-button>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('dynamicValidateForm')">提交</el-button>
        <el-button @click="addDomain">新增场景</el-button>
        <el-button @click="resetForm('dynamicValidateForm')">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'CompletionModel',
  inject: ['reload'],
  data() {
    return {
      dynamicValidateForm: {
        domains: [
          {
            value: ''
          }
        ]
      },
      formLabelWidth: '120px'
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          alert('提交成功')
          this.addModel()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    addModel() {
      console.log(this.dynamicValidateForm.domains)
      this.$http
        .post('http://127.0.0.1:8000/api/add_model', this.dynamicValidateForm.domains)
        .then(response => {
          console.log(response)
          this.res = response.data.result
        })
        .catch(function(error) {
          console.log(error)
        })
      this.reload()
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
    }
  }
}
</script>

<style scoped></style>
