<template>
  <el-row :gutter="20">
    <el-card class="box-card" style="height: 700px">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column label="项目id" width="180">
          <template slot-scope="scope">
            <!--        <i class="el-icon-time"></i>-->
            <span style="margin-left: 10px">{{ scope.row.date }}</span>
          </template>
        </el-table-column>
        <el-table-column label="项目名称" width="180">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>名称: {{ scope.row.name }}</p>
              <p>备注: {{ scope.row.address }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium" @click="gotolink">{{ scope.row.name }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click.native.prevent="handleDelete(scope.$index, tableData)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top: 20px;text-align: center">
        <el-button type="primary" round @click.prevent="addItem">
          添加项目
        </el-button>
      </div>
    </el-card>
  </el-row>
</template>

<script>
export default {
  data() {
    return {
      tableData: [
        {
          date: '1',
          name: '项目1',
          address: 'aaaa'
        },
        {
          date: '2',
          name: '项目2',
          address: 'bbbb'
        },
        {
          date: '3',
          name: '项目3',
          address: 'cccc'
        },
        {
          date: '4',
          name: '项目4',
          address: 'dddd'
        }
      ]
    }
  },
  methods: {
    handleEdit(index, row) {
      console.log(index, row)
      this.$prompt('修改的内容', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      })
        .then(({ value }) => {
          this.$message({
            type: 'success',
            message: '你输入的内容是: ' + value
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          })
        })
    },
    handleDelete(index, rows) {
      rows.splice(index, 1)
    },
    gotolink() {
      this.$router.replace('/trace')
    },
    addItem() {
      var list = {
        date: '5',
        name: '项目5',
        address: 'test'
      }
      this.tableData.push(list)
    }
  }
}
</script>

<style lang="scss" scoped>
@import '~@/assets/scss/item.scss';
</style>
