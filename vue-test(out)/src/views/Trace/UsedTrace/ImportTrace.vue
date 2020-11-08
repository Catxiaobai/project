<template>
  <div>
    <el-card>
      <el-upload action="http://127.0.0.1:8000/api/upload_file" :on-success="handleSuccess" :on-preview="handlePreview">
        <el-button type="primary">导入场景</el-button>
        <div slot="tip" class="el-upload__tip" style="font-size: medium">只能上传txt文件，并要求按标准格式撰写</div>
      </el-upload>
      <!--      <i :class="'el-icon-tickets'" style="font-size: 16px;margin-top: 10px"></i>-->
      <!--      <span>样例文本.txt</span>-->
      <!--      <el-button icon="el-icon-tickets" style="border: none;padding: 16px" class="test_txt" @click="downloadExample">样例文本.txt</el-button>-->
      <span style="font-size: 20px;margin-top: 100px">点击下载样例文本:</span>
      <i :class="'el-icon-tickets'" style="font-size: 16px;margin-top: 10px;margin-left:10px;color: #38b2ff"></i>
      <a href="/test.txt" download="使用场景样例文本.txt" style="color: #38b2ff">使用场景样例文本.txt</a>
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
  created() {
    console.log()
  },
  methods: {
    handleSuccess(code, file) {
      console.log(file.name)
      this.$http
        .post('http://127.0.0.1:8000/api/import_trace', { name: file.name, code: code, file: file })
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
    },
    downloadExample() {
      console.log('下载')
      // this.$http
      //   .get('http://127.0.0.1:8000/api/file_download')
      //   .then(response => {
      //     console.log(response.data)
      //     // this.linkDataArray = response.data.data_edge
      //     // this.nodeDataArray = response.data.data_node
      //     // this.text_data.nodeDataArray = this.nodeDataArray
      //     // this.text_data.linkDataArray = this.linkDataArray
      //     // // console.log(this.text_data)
      //     // this.load()
      //   })
      //   .catch(function(error) {
      //     console.log(error)
      //   })
      let blob = new Blob([], {
        type: 'text/csv;charset=GBK;'
      })
      let objUrl = URL.createObjectURL(blob)
      console.log(objUrl)
    }
  }
}
</script>

<style lang="scss" scoped>
.test_txt:hover {
  background-color: white;
}
.test_txt:visited {
  background: #ffffff;
}
.test_txt:focus {
  background: #ffffff;
}
</style>
