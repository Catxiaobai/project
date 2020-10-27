<template>
  <div id="personnel">
    <div id="item">
      <el-card class="tableTitle">
        <span style="font-size: 20px;margin-left: 45%">人员表</span>
        <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 300px; width: 300px" @input="pageList" />
        <!--        <el-button size="20px" type="primary" style="margin-left: 350px" @click="handleAdd('addForm')" icon="el-icon-plus">创建新项目</el-button>-->
        <!--        <el-button size="20px" type="primary" @click="handleAddBasedExist('addForm2')" icon="el-icon-plus">基于已有项目新建</el-button>-->
        <el-table :data="tableData" style="width: 100%;margin-top: 40px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
          <el-table-column label="序号" width="180px" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column label="工号" width="180px" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.number }}</span>
            </template>
          </el-table-column>
          <el-table-column label="姓名" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.name }}</span>
            </template>
          </el-table-column>
          <el-table-column label="所属单位" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.loc }}</span>
            </template>
          </el-table-column>
          <el-table-column label="权限" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.level }}</span>
            </template>
          </el-table-column>
          <!--          <el-table-column label="操作" align="center">-->
          <!--            <template slot-scope="scope">-->
          <!--              <el-button size="mini" type="success" @click="handleOpen(scope.$index, scope.row)">进入</el-button>-->
          <!--              &lt;!&ndash;            <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>&ndash;&gt;-->
          <!--              <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>-->
          <!--              <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>-->
          <!--            </template>-->
          <!--          </el-table-column>-->
        </el-table>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="page"
          :page-sizes="[1, 2, 5, 7, 10]"
          :page-size="limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          style="margin-left: 30%;margin-top: 30px"
        >
        </el-pagination>
      </el-card>
      <div id="add">
        <el-dialog title="添加新的项目" :visible.sync="visible.addDialog" center @close="resetForm('addForm')">
          <el-form :model="addForm" :rules="rules" ref="addForm">
            <el-form-item label="名称" label-width="120px" prop="name">
              <el-input v-model="addForm.name" clearable placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item label="项目介绍" label-width="120px" prop="introduction">
              <el-input v-model="addForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
            <el-button type="primary" @click="handleAddCommit('addForm')">确 定</el-button>
          </div>
        </el-dialog>
      </div>
      <div id="add2">
        <el-dialog title="基于已有项目添加" :visible.sync="visible.addDialog2" center>
          <el-form :model="addForm2" :rules="rules" ref="addForm">
            <el-form-item label="名称" label-width="120px" prop="name">
              <el-input v-model="addForm2.name" clearable placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item label="项目介绍" label-width="120px" prop="introduction">
              <el-input v-model="addForm2.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
            </el-form-item>
            <el-form-item label="基于的项目" label-width="120px" prop="basedItem">
              <el-select v-model="addForm2.basedItem" placeholder="请选择">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"> </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
            <el-button type="primary" @click="handleAddCommit2('addForm2')">确 定</el-button>
          </div>
        </el-dialog>
      </div>
      <div id="edit">
        <el-dialog title="编辑项目" :visible.sync="visible.editDialog" center>
          <el-form :model="editForm" :rules="rules" ref="editForm">
            <el-form-item label="名称" label-width="120px" prop="name">
              <el-input v-model="editForm.name" clearable placeholder="请输入名称"></el-input>
            </el-form-item>
            <el-form-item label="项目介绍" label-width="120px" prop="introduction">
              <el-input v-model="editForm.introduction" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入项目介绍"> </el-input>
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <!--          <el-button @click="visible.addDialog = false">取 消</el-button>-->
            <el-button type="primary" @click="handleEditCommit('editForm')">确 定</el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Personnel.vue',
  data() {
    return {
      limit: 7, //每页显示条数
      total: 0, //项目总数
      page: 1, //第几页
      search: '', //搜索框
      tableData: [
        {
          id: '1',
          number: '20201026',
          name: '张一',
          loc: '张一的单位',
          level: '管理员'
        },
        {
          id: '2',
          number: '20201027',
          name: '张二',
          loc: '张二的单位',
          level: '普通成员'
        },
        {
          id: '3',
          number: '20201027',
          name: '张三',
          loc: '张三的单位',
          level: '普通成员'
        },
        {
          id: '4',
          number: '20201029',
          name: '张四',
          loc: '张四的单位',
          level: '管理员'
        }
      ], //项目表
      showItem: {}, //查看项目
      visible: {
        addDialog: false,
        addDialog2: false,
        deleteDialog: false,
        editDialog: false
      },
      editForm: {
        //修改时使用
        id: '',
        name: '',
        introduction: ''
      },
      addForm: {
        //添加使用
        name: '',
        introduction: ''
      },
      addForm2: {
        //添加使用
        name: '',
        introduction: '',
        basedItem: ''
      },
      deleteData: [],
      rules: {
        name: [{ required: true, message: '不能为空', trigger: 'blur' }],
        introduction: [{ required: true, message: '不能为空', trigger: 'blur' }]
      },
      options: []
    }
  }
}
</script>

<style scoped></style>
