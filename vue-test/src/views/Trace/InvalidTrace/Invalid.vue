<template>
  <div>
    <!--    标题-->
    <el-card class="tableTitle">
      <span style="font-size: 20px">当前项目共有{{ total }}条失效场景</span>
      <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
      <el-button size="20px" type="success" style="margin-left: 480px" @click="handleAdd" icon="el-icon-plus">添加新场景</el-button>
    </el-card>
    <!--    表格内容-->
    <el-card class="traceTable" style="margin-top: 20px">
      <el-table :data="tableData" style="width: 100%;" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
        <el-table-column label="序号" width="50px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.invalid_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="名称" width="120px" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.invalid_name }}</span>
          </template>
        </el-table-column>
        <el-table-column label="失效场景" align="center">
          <template slot-scope="scope">
            <span style="margin-left: 10px">{{ scope.row.invalid_content }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="350px">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>
            <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!--    分页显示-->
    <el-card class="tablePage" style="margin-top: 20px">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="page"
        :page-sizes="[1, 2, 4, 8]"
        :page-size="limit"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-left: 30%"
      >
      </el-pagination>
    </el-card>
    <!--    查看trace弹窗-->
    <!--    todo: 展示效果不好-->
    <el-dialog title="暂定以弹窗形式呈现" :visible.sync="dialogShowTrace">
      <span style="display: block">场景名称：{{ showTrace.invalid_name }}</span>
      <span style="margin-top: 10px;display: block">场景内容：</span>
      <span style="display: block;white-space: pre-line">{{ showTrace.invalid_content }}</span>
      <span style="margin-top: 10px;display: block;white-space: pre-line">场景描述：{{ showTrace.invalid_details }}</span>
      <span slot="footer" class="dialog-footer">
        <!--        <el-button @click="dialogShowTrace = false">取 消</el-button>-->
        <el-button type="primary" @click="dialogShowTrace = false">OK</el-button>
      </span>
    </el-dialog>
    <!--    添加场景弹窗-->
    <el-dialog title="添加场景" :visible.sync="dialogAddTrace">
      <el-form :model="addForm">
        <el-form-item label="场景名称" label-width="120px">
          <el-input v-model="addForm.name" clearable placeholder="请输入场景名称"></el-input>
        </el-form-item>
        <el-form-item label="场景内容" label-width="120px">
          <el-input v-model="addForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景具体内容"> </el-input>
        </el-form-item>
        <el-form-item label="场景描述" label-width="120px">
          <el-input v-model="addForm.details" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景文字描述"> </el-input>
        </el-form-item>
        <el-form-item label="场景介绍" label-width="120px">
          <el-input v-model="addForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景简单介绍"> </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogAddTrace = false">取 消</el-button>
        <el-button type="primary" @click="handleAddCommit">确 定</el-button>
      </div>
    </el-dialog>
    <!--    编辑场景弹窗-->
    <el-dialog title="编辑此场景" :visible.sync="dialogEditTrace">
      <el-form :model="editForm">
        <el-form-item label="场景名称" label-width="120px">
          <el-input v-model="editForm.name" clearable placeholder="请输入场景名称"></el-input>
        </el-form-item>
        <el-form-item label="场景内容" label-width="120px">
          <el-input v-model="editForm.content" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景具体内容"> </el-input>
        </el-form-item>
        <el-form-item label="场景描述" label-width="120px">
          <el-input v-model="editForm.details" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景文字描述"> </el-input>
        </el-form-item>
        <el-form-item label="场景介绍" label-width="120px">
          <el-input v-model="editForm.describe" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入场景简单介绍"> </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogEditTrace = false">取 消</el-button>
        <el-button type="primary" @click="handleEditCommit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'UsedTrace.vue',
  data() {
    return {
      limit: 4, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      search: '', //搜索框
      dialogShowTrace: false, //查看trace弹窗
      dialogAddTrace: false, //添加trace弹窗
      dialogEditTrace: false, //编辑trace
      tableData: [], //trace表
      showTrace: {}, //查看trace
      addForm: {
        //添加时使用
        name: '',
        content: '',
        details: '',
        describe: ''
      },
      editForm: {
        id: '',
        name: '',
        content: '',
        details: '',
        describe: ''
      } //添加trace
    }
  },
  created() {
    this.pageList()
  },
  methods: {
    pageList() {
      // 发请求拿到数据并暂存全部数据,方便之后操作
      this.$http
        .get('http://127.0.0.1:8000/api/invalid_list')
        .then(response => {
          console.log(response.data.invalid_list)
          this.data = response.data.invalid_list
          this.getList()
        })
        .catch(function(error) {
          console.log(error)
        })
      // this.data = this.tableData
      // this.getList()
    },
    // 处理数据
    getList() {
      // es6过滤得到满足搜索条件的展示数据list
      // eslint-disable-next-line no-unused-vars
      // console.log({ test: this.search })
      let list = this.data.filter((item, index) => item.invalid_content.includes(this.search))
      // let list = this.data
      this.tableData = list.filter((item, index) => index < this.page * this.limit && index >= this.limit * (this.page - 1))
      this.total = list.length
    },
    // 当每页数量改变
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`)
      this.limit = val
      this.getList()
    },
    // 当当前页改变
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`)
      this.page = val
      this.getList()
    },
    handleShow(index, row) {
      this.dialogShowTrace = true
      // console.log(index, row)
      this.showTrace = row
    },
    handleEdit(index, row) {
      // console.log(index, row)
      this.editForm.id = row.invalid_id
      this.editForm.name = row.invalid_name
      this.editForm.content = row.invalid_content
      this.editForm.describe = row.invalid_describe
      this.editForm.details = row.invalid_details
      this.dialogEditTrace = true
    },
    handleDelete(index, row) {
      // console.log(index, row)
      this.$confirm('此操作将删除该trace, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          console.log(row.invalid_id)
          this.$http
            .post('http://127.0.0.1:8000/api/delete_invalid', { invalid_id: row.invalid_id })
            .then(response => {
              console.log(response.data)
              if (response.data.error_code === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功!'
                })
                this.pageList()
              }
            })
            .catch(function(error) {
              console.log(error)
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    handleAdd() {
      this.dialogAddTrace = true
    },
    handleAddCommit() {
      this.dialogAddTrace = false
      console.log(this.addForm)
      this.$http
        .post('http://127.0.0.1:8000/api/add_invalid', this.addForm)
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.pageList()
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    handleEditCommit() {
      this.dialogEditTrace = false
      console.log(this.addForm)
      this.$http
        .post('http://127.0.0.1:8000/api/edit_invalid', this.editForm)
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.pageList()
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
}
</script>

<style lang="scss" scoped></style>
