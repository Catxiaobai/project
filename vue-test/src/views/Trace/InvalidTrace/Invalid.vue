<template>
  <div>
    <div class="invalidForm" v-show="divMain">
      <!--    标题-->
      <el-card class="tableTitle">
        <span style="font-size: 20px">当前项目共有{{ total }}条风险场景</span>
        <el-input v-model="search" placeholder="输入关键字搜索" style="margin-left: 30px; width: 300px" @input="pageList" />
        <el-button size="20px" type="success" style="margin-left: 480px" @click="handleAdd" icon="el-icon-plus">添加新场景</el-button>
        <!--      </el-card>-->
        <!--      &lt;!&ndash;    表格内容&ndash;&gt;-->
        <!--      <el-card class="traceTable" style="margin-top: 20px">-->
        <el-table :data="tableData" style="width: 100%;margin-top: 20px" stripe border :header-cell-style="{ background: '#eef1f6', color: '#606266' }">
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
          <el-table-column label="风险场景" align="center">
            <template slot-scope="scope">
              <span style="margin-left: 10px">{{ scope.row.invalid_content }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" width="350px">
            <template slot-scope="scope">
              <el-button size="mini" type="info" @click="handleShow(scope.$index, scope.row)">查看</el-button>
              <el-button size="mini" type="primary" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              <el-button size="mini" type="warning" @click="handleVerify(scope.$index, scope.row)">触发</el-button>
            </template>
          </el-table-column>
        </el-table>
        <!--      </el-card>-->
        <!--      &lt;!&ndash;    分页显示&ndash;&gt;-->
        <!--      <el-card class="tablePage" style="margin-top: 20px">-->
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="page"
          :page-sizes="[1, 2, 4, 7, 10]"
          :page-size="limit"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          style="margin-left: 30%;margin-top: 20px"
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
      <!--    提示不能触发的弹窗-->
      <el-dialog title="提示" :visible.sync="dialogVerify" width="30%">
        <span>此场景无法触发，验证结果为安全</span>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVerify = false">取 消</el-button>
          <el-button type="primary" @click="dialogVerify = false">确 定</el-button>
        </span>
      </el-dialog>
    </div>
    <div class="drawLine" v-show="divDraw">
      <el-card style="height: 560px">
        <!--      <span style="font-size: x-large;margin-left: 40%">模型可视化</span>-->
        <el-col :span="12">
          <span style="font-size: x-large;margin-left: 40%">风险场景触发</span>
          <div id="myDiagramDiv" class="myDiagramDiv"></div>
        </el-col>
        <el-col :span="12">
          <el-button type="danger" style="float: right" @click="closeDivDraw">关闭</el-button>
          <div class="text-path">
            <p>触发路径</p>
            <br />
            <span style="white-space: normal">{{ test_draw }}</span>
          </div>
        </el-col>
      </el-card>
    </div>
  </div>
</template>

<script>
import go from 'gojs'
const MAKE = go.GraphObject.make
export default {
  name: 'UsedTrace.vue',
  inject: ['reload'],
  data() {
    return {
      limit: 7, //每页显示条数
      total: null, //trace总数
      page: 1, //第几页
      search: '', //搜索框
      dialogShowTrace: false, //查看trace弹窗
      dialogAddTrace: false, //添加trace弹窗
      dialogEditTrace: false, //编辑trace
      dialogVerify: false, //验证结果
      divMain: true,
      divDraw: false,
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
      },
      nodeDataArray: [],
      linkDataArray: [],
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: []
      },
      test_draw: []
    }
  },
  created() {
    this.pageList()
    this.getData()
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
    },
    handleVerify(index, row) {
      console.log(index, row)
      this.$http
        .post('http://127.0.0.1:8000/api/verify_invalid', { invalid: row })
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            // this.pageList()
            // console.log('验证成功')
            if (response.data.res === 'danger') {
              // todo: 画图
              // this.init()
              this.getPathData()
              this.drawlink()
              this.divDraw = true
              this.divMain = false
              // window.open('http://localhost:2333/#/pageFive')
            } else {
              // todo: 弹窗提示不能触发
              this.dialogVerify = true
            }
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    closeDivDraw() {
      this.reload()
      // this.divMain = true
      // this.divDraw = false
    },
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.postData(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
    },
    load() {
      var model = go.Model.fromJson(this.text_data)

      model.makeUniqueKeyFunction = function(model, data) {
        var i = model.nodeDataArray.length * 2 + 1
        while (model.findNodeDataForKey(i) !== null) i += 2
        data.id = i // assume Model.nodeKeyProperty === "id"
        return i
      }
      // link data id's are even numbers
      model.makeUniqueLinkKeyFunction = function(model, data) {
        var i = model.linkDataArray.length * 2 + 2
        while (model.findLinkDataForKey(i) !== null) i += 2
        data.id = i // assume GraphLinksModel.linkKeyProperty === "id"
        return i
      }
      this.myDiagram.model = model
    },
    getData() {
      this.$http
        .get('http://127.0.0.1:8000/api/deliver_model')
        .then(response => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // this.test_draw = [1, 2, 2, 3]
          // console.log(this.text_data)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    getPathData() {
      this.$http
        .get('http://127.0.0.1:8000/api/verify_safe_result')
        .then(response => {
          console.log(response.data)
          this.test_draw = response.data.data_path
          // this.test_draw = [1, 2, 2, 3]
          // console.log(this.test_draw)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    postData(data) {
      this.$http
        .post('http://127.0.0.1:8000/api/verify_action', { add: data })
        .then(response => {
          console.log(response.data)
          if (response.data.error_code === 0) {
            this.$message({
              type: 'success',
              message: response.data.result
            })
          }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    init() {
      var element = document.getElementById('mytest')
      var $ = go.GraphObject.make
      this.myDiagram = $(go.Diagram, 'myDiagramDiv', {
        // have mouse wheel events zoom in and out instead of scroll up and down
        'toolManager.mouseWheelBehavior': go.ToolManager.WheelZoom,
        // support double-click in background creating a new node
        'clickCreatingTool.archetypeNodeData': { text: 'new node' },
        // InitialLayoutCompleted: function(e) {
        isReadOnly: true,
        // enable undo & redo
        'undoManager.isEnabled': false,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 40,
          defaultElectricalCharge: 180,
          randomNumberGenerator: null,
          infinityDistance: 210
        })
      })

      this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))) // end of Adornment
        },
        new go.Binding('location', 'loc', go.Point.parse).makeTwoWay(go.Point.stringify),
        // define the node's outer shape, which will surround the TextBlock

        // 图标的style
        $(go.Shape, 'Circle', new go.Binding('fill', 'color'), {
          desiredSize: new go.Size(67, 67),
          fill: $(go.Brush, 'Linear', { 0: 'rgb(0,191,255)', 1: 'rgb(30,144,255)' }),
          stroke: 'black',
          portId: '',
          fromLinkable: true,
          fromLinkableSelfNode: true,
          fromLinkableDuplicates: true,
          toLinkable: true,
          toLinkableSelfNode: true,
          toLinkableDuplicates: true,
          cursor: 'pointer'
        }),
        // 字体的style
        $(
          go.TextBlock,
          {
            font: 'bold 11pt helvetica, bold arial, sans-serif',
            editable: true // editing the text automatically updates the model data
          },
          new go.Binding('text', 'text').makeTwoWay()
        )
      )
      this.myDiagram.toolManager.hoverDelay = 10

      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('LinkRelinked', function(e) {
        console.log('线重连')
        // var data = { test: 'testjson' }
        // postDelData(data)
      })
      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('TextEdited', function(e) {
        console.log('文本编辑' + e)
      })

      // 监听删除事件
      this.myDiagram.addDiagramListener('SelectionDeleted', function(e) {
        console.log(e)
        e.subject.each(function(n) {
          // console.log('delete:' + JSON.stringify(n.data))
          //
          // console.log('total:' + e.diagram.model.toJson())
          // 传递删除信息和剩下的信息
          var data = { total: e.diagram.model.toJson(), delete: JSON.stringify(n.data) }
          postDelData(data)
        })
      })
      // 监听添加事件
      this.myDiagram.addDiagramListener('LinkDrawn', function(e) {
        console.log('add:' + JSON.stringify(e.subject.data))
        console.log('total:' + e.diagram.model.toJson())
        // 传递添加的信息和剩下的信息
        var data = { total: e.diagram.model.toJson(), add: JSON.stringify(e.subject.data) }
        postAddData(data)
      })
      // 向后端传递添加信息
      function postAddData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', 'http://127.0.0.1:8000/api/verify_add', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function() {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      // 向后端传递添删除信息
      function postDelData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', 'http://127.0.0.1:8000/api/verify_del', true) //第二步：打开连接
        httpRequest.setRequestHeader('Content-type', 'application/json') //设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
        httpRequest.send(JSON.stringify(data)) //发送请求 将情头体写在send中
        /**
         * 获取数据后的处理程序
         */
        httpRequest.onreadystatechange = function() {
          //请求后的回调接口，可将请求成功后要执行的程序写在其中
          if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            //验证请求是否发送成功
            var json = JSON.parse(httpRequest.responseText) //获取到服务端返回的数据
            console.log(json)
            element.value = json['result']
            myFunction(json['result'])
          }
        }
      }
      function myFunction(res) {
        var x
        var r = confirm(res)
        if (r == true) {
          x = '你按下了"确定"按钮!'
        } else {
          x = '你按下了"取消"按钮!'
        }
        // document.getElementById('demo').innerHTML = x
      }
      function test(str) {
        console.log(element)
        element.value = str
        // console.log(element.value)
      }

      // unlike the normal selection Adornment, this one includes a Button
      this.myDiagram.nodeTemplate.selectionAdornmentTemplate = $(
        go.Adornment,
        'Spot',
        $(
          go.Panel,
          'Auto',
          $(go.Shape, { fill: null, stroke: 'blue', strokeWidth: 2 }),
          $(go.Placeholder) // this represents the selected Node
        )
        // the button to create a "next" node, at the top-right corner
        // $(
        //   'Button',
        //   {
        //     alignment: go.Spot.TopRight,
        //     click: addNodeAndLink // this function is defined below
        //   },
        //   $(go.Shape, 'PlusLine', { desiredSize: new go.Size(6, 6) })
        // ) // end button
      ) // end Adornment
      // and adds a link to that new node
      function addNodeAndLink(e, obj) {
        var adorn = obj.part
        e.handled = true
        var diagram = adorn.diagram
        diagram.startTransaction('Add State')

        // get the node data for which the user clicked the button
        var fromNode = adorn.adornedPart
        var fromData = fromNode.data
        // create a new "State" data object, positioned off to the right of the adorned Node
        var toData = { text: 'new' }
        var p = fromNode.location.copy()
        p.x += 100
        toData.loc = go.Point.stringify(p) // the "loc" property is a string, not a Point object
        // add the new node data to the model
        var model = diagram.model
        model.addNodeData(toData)

        // create a link data from the old node data to the new node data
        var linkdata = {
          from: model.getKeyForNodeData(fromData), // or just: fromData.id
          to: model.getKeyForNodeData(toData),
          text: 'transition'
        }
        // and add the link data to the model
        model.addLinkData(linkdata)

        // select the new Node
        var newnode = diagram.findNodeForData(toData)
        diagram.select(newnode)

        diagram.commitTransaction('Add State')

        // if the new node is off-screen, scroll the diagram to show the new node
        diagram.scrollToRect(newnode.actualBounds)
      }

      // this.myDiagram.addDiagramListener('addNodeAndLink', function() {
      //   console.log('test')
      // })
      // replace the default Link template in the linkTemplateMap
      this.myDiagram.linkTemplate = $(
        go.Link, // the whole link panel
        {
          curve: go.Link.Bezier,
          adjusting: go.Link.Stretch,
          reshapable: true,
          relinkableFrom: true,
          relinkableTo: true
        },
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $(
            'ToolTip',
            { 'Border.fill': 'whitesmoke', 'Border.stroke': 'black' },
            $(go.TextBlock, { margin: 4 }, new go.Binding('text', '', tooltipTextConverter))
          )
        },
        {
          click: function(e, obj) {
            console.log('e:' + e + '---obj:' + obj.part.data)
            console.log('Clicked on ' + obj.part.data.key)
          }
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          new go.Binding('stroke', 'color'),
          new go.Binding('strokeWidth', 'mySize'),
          { strokeWidth: 1.5 }
        ),
        $(
          go.Shape, // the arrowhead
          { toArrow: 'standard', stroke: null }
        ),
        $(
          go.Panel,
          'Auto',
          $(
            go.Shape, // the label background, which becomes transparent around the edges
            {
              fill: $(go.Brush, 'Radial', { 0: 'rgb(240, 240, 240)', 0.3: 'rgb(240, 240, 240)', 1: 'rgba(240, 240, 240, 0)' }),
              stroke: null
            }
          ),
          $(
            go.TextBlock,
            'transition', // the label text
            {
              textAlign: 'center',
              font: '10pt helvetica, arial, sans-serif',
              stroke: 'black',
              margin: 4,
              editable: true // editing the text automatically updates the model data
            },
            new go.Binding('text', 'text').makeTwoWay()
          )
        )
      )
      function tooltipTextConverter(person) {
        var str = ''
        // console.log(person)
        // str += 'id: ' + person.id + '\n'
        str += 'name: ' + person.text + '\n'
        str += 'source: ' + person.from + '\n'
        str += 'target: ' + person.to + '\n'
        str += 'event: ' + person.event + '\n'
        str += 'condition: ' + person.cond + '\n'
        str += 'action: ' + person.action + '\n'
        return str
      }
    },
    drawlink() {
      // function change() {
      //   var test_draw = [1, 2, 3]
      //   var ttt = this.myDiagram.findLinkForKey(1).data
      //   this.myDiagram.model.setDataProperty(ttt, 'color', 'blue')
      // }
      // var test_draw = [1, 2, 2, 3]
      var temp = 0
      var flag_list = []
      Array.prototype.remove = function(val) {
        var index = this.indexOf(val)
        if (index > -1) {
          this.splice(index, 1)
        }
      }
      console.log(this.text_data)
      var T = setInterval(() => {
        //temp += Math.floor(Math.random() * 10 + 1)
        //this.percent += Math.floor(Math.random() * 10 + 1)
        // var cuttent_data = this.test_draw[temp]
        if (flag_list.indexOf(this.test_draw[temp]) > -1) {
          flag_list.remove(this.test_draw[temp])
          var ttt = this.myDiagram.findLinkForKey(this.test_draw[temp]).data
          this.myDiagram.model.setDataProperty(ttt, 'color', 'blue')
          this.myDiagram.model.setDataProperty(ttt, 'mySize', '5')
          temp -= 1
        } else {
          flag_list.push(this.test_draw[temp])
          var tt = this.myDiagram.findLinkForKey(this.test_draw[temp]).data
          this.myDiagram.model.setDataProperty(tt, 'color', 'red')
          this.myDiagram.model.setDataProperty(tt, 'mySize', '5')
        }
        // if(temp<this.text_data.length-1){}
        temp += 1
        if (temp >= this.test_draw.length) clearInterval(T)
      }, 1000)
      //window.setInterval(change, 1000)
    }
  },
  mounted() {
    this.init()
  }
}
</script>

<style lang="scss" scoped>
.myDiagramDiv {
  background-color: whitesmoke;
  border: solid 1px black;
  width: 100%;
  height: 500px;
  //margin-top: 20px;
}
.text-path {
  text-align: center;
  font-size: xx-large;
}
</style>
