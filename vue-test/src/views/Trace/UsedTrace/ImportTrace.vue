<template>
  <div>
    <el-card>
      <el-upload action="https://jsonplaceholder.typicode.com/posts/" :on-success="handleSuccess" :on-preview="handlePreview">
        <el-button size="small" type="primary">导入场景</el-button>
        <div slot="tip" class="el-upload__tip">只能上传txt文件，并要求按标准格式撰写</div>
      </el-upload>
    </el-card>

    <el-card style="margin-top: 20px">
      <!--      <span style="display: block">这是上传的文件信息</span>-->
      <span style="display: block;white-space: pre-line">{{ msg }}</span>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: '这里展示导入文件内容'
    }
  },
  methods: {
    handleSuccess(code, file) {
      console.log(file.name)
      this.$http
        .post('http://127.0.0.1:8000/api/import_trace', { name: file.name })
        .then(response => {
          if (response.data.error_code === 0) {
            console.log(response)
            this.msg = '场景导入成功\n\n' + response.data.content
          } else {
            // console.log(response.data)
            this.msg = response
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    handlePreview(file) {
      console.log(file)
    }
  }
}
</script>

<style lang="scss" scoped></style>
