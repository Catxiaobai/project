<!--<template>-->
<!--  <div id="app">-->
<!--    <input type="button" value="导入" id="fileImport" v-on:click="clickLoad" style="background: green; height: 80px; width: 100px; font-size: 28px;" />-->
<!--    <input type="file" id="files" ref="refFile" style="display: none" v-on:change="fileLoad" />-->
<!--    <div>-->
<!--      <h1>testTxt</h1>-->
<!--    </div>-->
<!--  </div>-->
<!--</template>-->
<!--<script>-->
<!--export default {-->
<!--  data() {-->
<!--    return {-->
<!--      name: 'E:/Code/301temp/Model3/out.txt',-->
<!--      testTXT: require('../assets/txtFile/test.txt')-->
<!--    }-->
<!--  },-->
<!--  methods: {-->
<!--    clickLoad() {-->
<!--      // this.$refs.refFile.dispatchEvent(new MouseEvent('click'))-->
<!--    },-->
<!--    fileLoad() {-->
<!--      // const selectedFile = this.$refs.refFile.files[0]-->

<!--      const selectedFile = function(name) {-->
<!--        let xhr = new XMLHttpRequest(),-->
<!--          okStatus = document.location.protocol === 'file:' ? 0 : 200-->
<!--        xhr.open('GET', name, false)-->
<!--        xhr.overrideMimeType('text/html;charset=utf-8') //默认为utf-8-->
<!--        xhr.send(null)-->
<!--        return xhr.status === okStatus ? xhr.responseText : null-->
<!--      }-->
<!--      var reader = new FileReader()-->
<!--      reader.readAsText(selectedFile)-->
<!--      reader.onload = function() {-->
<!--        console.log(this.result)-->
<!--      }-->
<!--    }-->
<!--  }-->
<!--}-->
<!--</script>-->
