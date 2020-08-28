<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="场景id">
      <el-input v-model="form.id"></el-input>
    </el-form-item>
    <el-form-item label="场景名称">
      <el-input v-model="form.name"></el-input>
    </el-form-item>
    <el-form-item label="场景内容">
      <el-input type="textarea" v-model="form.desc"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="onSubmit">立即添加</el-button>
      <el-button>取消</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      form: {
        id: '',
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('submit!')
    }
  }
}
</script>

<style scoped></style>
