<template>
  <div id="subCompleteness">
    <div class="divHelp">
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <p>此页面对模型进行完整性验证</p>
        <p>点击”完整性验证“按钮，即可开始验证</p>
        <br />
        <p style="font-weight: bold">若模型不完整</p>
        <p>左侧模型图中会提示需要补全的新状态,用红色标出</p>
        <p>右侧也会显示对应的文字结果</p>
        <p>可以点击“全部补全”按钮，即可将所有提示的状态全部补全</p>
        <p>也可以在图中逐个补全，鼠标左键双击待补全的节点或边，会出现提示弹窗，点击确定即可补全</p>
        <el-button icon="el-icon-message-solid" circle slot="reference"></el-button>
      </el-popover>
      <el-popover placement="bottom" trigger="click">
        <!--        <el-button slot="reference">click 激活</el-button>-->
        <div>
          <p>此页面对模型进行完整性验证</p>
          <p>点击”完整性验证“按钮，即可开始验证</p>
          <br />
          <p style="font-weight: bold">若模型不完整</p>
          <p>左侧模型图中会提示需要补全的新状态,用红色标出</p>
          <p>右侧也会显示对应的文字结果</p>
          <p>可以点击“全部补全”按钮，即可将所有提示的状态全部补全</p>
          <p>也可以在图中逐个补全，鼠标左键双击待补全的节点或边，会出现提示弹窗，点击确定即可补全</p>
        </div>
        <el-button type="text" slot="reference">操作提示</el-button>
      </el-popover>
    </div>
    <el-card style="height: 600px">
      <el-col :span="14">
        <div id="myDiagramDiv" class="myDiagramDiv"></div>
        <el-button type="primary" style="margin-left: 25%;margin-top: 10px" @click="reduction">模型还原</el-button>
        <el-button type="primary" style="margin-left: 60px" @click="judge">完整性验证</el-button>
      </el-col>
      <el-col :span="10">
        <div class="text-path">
          <p>验证结果</p>
          <br />
          <p style="background: blanchedalmond">{{ msg.res }}</p>
          <br />
          <p>{{ msg.tip }}</p>
          <p>{{ msg.node }}</p>
          <p>{{ msg.edge }}</p>
          <el-button type="primary" v-show="textVisible" style="margin-top: 60px" @click="completeAll">全部补全</el-button>
        </div>
      </el-col>
    </el-card>
  </div>
</template>

<script>
import go from 'gojs'

const MAKE = go.GraphObject.make
export default {
  name: 'subCompleteness.vue',
  inject: ['reload'],
  data() {
    return {
      nodeDataArray: [],
      linkDataArray: [],
      text_data: {
        // class: 'go.GraphLinksModel',
        nodeKeyProperty: 'id',
        linkKeyProperty: 'id',
        nodeDataArray: [],
        linkDataArray: []
      },
      msg: {
        res: '',
        tip: '',
        node: '',
        edge: '',
        node_id: [],
        edge_id: []
      },
      msgNode: '',
      msgEdge: '',
      // msg: '',
      test: 'tets',
      textVisible: false
    }
  },
  mounted() {
    this.init()
  },
  created() {
    this.getData()
  },
  methods: {
    showIncremental(str) {
      // show the last transaction as an incremental update in JSON-formatted text
      var element = document.getElementById('myTransaction')
      // don't show anything upon the initial layout
      if (element.value === 'InitialLayout') str = ''
      element.value = str
    },
    save() {
      // document.getElementById('mySavedModel').value = this.myDiagram.model.toJson()
      console.log(this.myDiagram.model.toJson())
      this.postData(this.myDiagram.model.toJson())
      this.text_data = this.myDiagram.model.toJson()
      this.myDiagram.isModified = false
      this.showIncremental('')
    },
    load() {
      // var model = go.Model.fromJson(document.getElementById('mySavedModel').value)
      // establish GraphLinksModel functions:
      // node data id's are odd numbers
      var model = go.Model.fromJson(this.text_data)
      // console.log(this.text_data)
      // console.log(model.nodeDataArray)
      // console.log(document.getElementById('mySavedModel').value)
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
      this.showIncremental('')
    },
    getData() {
      this.$http
        .post(this.Global_Api + '/api/deliver_model_data', { type: 'complex', item: this.itemInfo })
        .then(response => {
          console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // console.log(this.text_data)
          this.load()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    postData: function(data) {
      this.$http
        .post(this.Global_Api + '/api/verify_action', { add: data })
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
        // isReadOnly: true,
        // enable undo & redo
        'undoManager.isEnabled': false,
        layout: $(go.ForceDirectedLayout, {
          defaultSpringLength: 40,
          defaultElectricalCharge: 180,
          randomNumberGenerator: null,
          infinityDistance: 215
        })
      })
      // 节点样式
      this.myDiagram.nodeTemplate = $(
        go.Node,
        'Auto',
        {
          cursor: 'pointer',
          // define a tooltip for each node that displays the color as text
          toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'name'))) // end of Adornment
        },
        {
          // click: function(e, obj) {
          //   console.log('e:' + e + '---obj:' + JSON.stringify(obj.part.data))
          //   console.log('Clicked on ' + obj.part.data.key)
          // }
          doubleClick: function(e, obj) {
            console.log('obj:' + JSON.stringify(obj.part.data))
            var rr = confirm('是否补全所选点' + JSON.stringify(obj.part.data.text))
            var aim_node = e.diagram.findNodeForKey(obj.part.data.id).data
            if (rr == true) {
              var data = { node: aim_node }
              postData(data)
              e.diagram.model.setDataProperty(aim_node, 'color', 'rgb(0,191,255)')
            } else {
              console.log(aim_node)
              e.diagram.model.removeNodeData(aim_node)
            }
          }
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
      // 边样式
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
          toolTip: $(
            'ToolTip',
            { 'Border.fill': 'whitesmoke', 'Border.stroke': 'black' },
            $(go.TextBlock, { margin: 4 }, new go.Binding('text', '', tooltipTextConverter))
          )
          // define a tooltip for each node that displays the color as text
          // toolTip: $('ToolTip', $(go.TextBlock, { margin: 4 }, new go.Binding('text', 'action'))) // end of Adornment
        },
        {
          // click: function(e, obj) {
          //   console.log('e:' + e + '---obj:' + JSON.stringify(obj.part.data))
          //   console.log('Clicked on ' + obj.part.data.key)
          // }
          doubleClick: function(e, obj) {
            console.log('obj:' + JSON.stringify(obj.part.data))
            var rr = confirm('是否补全所选边' + JSON.stringify(obj.part.data.text))
            var aim_link = e.diagram.findLinkForKey(obj.part.data.id).data
            console.log(aim_link)
            if (rr == true) {
              var data = { edge: aim_link }
              postData(data)
              e.diagram.model.setDataProperty(aim_link, 'color', 'black')
            } else {
              e.diagram.model.removeLinkData(aim_link)
            }
          }
        },
        new go.Binding('points').makeTwoWay(),
        new go.Binding('curviness', 'curviness'),
        $(
          go.Shape, // the link shape
          { strokeWidth: 1.5 },
          new go.Binding('stroke', 'color')
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
              fill: $(go.Brush, 'Radial', {
                0: 'rgb(240, 240, 240)',
                0.3: 'rgb(240, 240, 240)',
                1: 'rgba(240, 240, 240, 0)'
              }),
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

      this.myDiagram.toolManager.hoverDelay = 10

      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('LinkRelinked', function(e) {
        console.log('线重连')
        var data = { test: 'testjson' }
        postData(data)
      })
      //添加监听线重新连接事件
      this.myDiagram.addDiagramListener('TextEdited', function(e) {
        console.log('文本编辑' + e)
      })
      // //添加双击事件
      // this.myDiagram.addDiagramListener('ObjectDoubleClicked', function(e, obj) {
      //   console.log('双击事件' + obj)
      // })
      // 监听删除事件
      this.myDiagram.addDiagramListener('SelectionDeleted', function(e) {
        console.log(e)
        e.subject.each(function(n) {
          // console.log('delete:' + JSON.stringify(n.data))
          //
          // console.log('total:' + e.diagram.model.toJson())
          // 传递删除信息和剩下的信息
          var data = { total: e.diagram.model.toJson(), delete: JSON.stringify(n.data) }
          postData(data)
        })
      })
      // 监听添加事件
      this.myDiagram.addDiagramListener('LinkDrawn', function(e) {
        console.log('add:' + JSON.stringify(e.subject.data))
        console.log('total:' + e.diagram.model.toJson())
        // 传递添加的信息和剩下的信息
        var data = { total: e.diagram.model.toJson(), add: JSON.stringify(e.subject.data) }
        postData(data)
      })

      // 向后端传递变化信息
      function postData(data) {
        var httpRequest = new XMLHttpRequest() //第一步：创建需要的对象
        httpRequest.open('POST', this.Global_Api + '/api/save_node_and_link', true) //第二步：打开连接
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
          }
        }
      }
    },
    judge() {
      this.$http
        .post(this.Global_Api + '/api/verify_complete', { type: 'complex' })
        .then(response => {
          // console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // this.text_data.nodeDataArray.push(this.nodeDataArray[0])
          // this.text_data.linkDataArray.push(this.linkDataArray[0])
          console.log(this.text_data)
          this.result(response.data.data_node_add, response.data.data_edge_add, response.data.res)
          this.load()
        })
        .catch(function(error) {
          // console.log(error)
        })
    },
    result(node, edge, res) {
      // todo:展示验证结果
      console.log(node, edge, res)
      if (res === 'Y') {
        this.msg.res = '检测到模型完整'
        this.msg.tip = ''
        this.msg.node = ''
        this.msg.edge = ''
        this.msg.node_id = []
        this.msg.edge_id = []
        this.textVisible = false
      } else if (res === 'N') {
        this.msg.res = '检测到模型不完整'
        this.msg.tip = '建议添加：'
        this.msg.node = 'node: '
        for (var i = 0; i < node.length; i++) {
          this.msg.node += JSON.stringify(node[i].text)
          this.msg.node_id.push(JSON.stringify(node[i].id))
        }
        this.msg.edge = ' edge: '
        for (var j = 0; j < edge.length; j++) {
          this.msg.edge += JSON.stringify(edge[j].text)
          this.msg.edge_id.push(JSON.stringify(edge[j].id))
        }
        // this.msg.node_id = JSON.stringify(node[0].id)
        // this.msg.edge_id = JSON.stringify(edge[0].id)
        this.textVisible = true
      }
      this.$http
        .get(this.Global_Api + '/api/verify_complete')
        .then(response => {
          // console.log(response.data)
          this.linkDataArray = response.data.data_edge
          this.nodeDataArray = response.data.data_node
          this.text_data.nodeDataArray = this.nodeDataArray
          this.text_data.linkDataArray = this.linkDataArray
          // this.text_data.nodeDataArray.push(this.nodeDataArray[0])
          // this.text_data.linkDataArray.push(this.linkDataArray[0])
          console.log(this.text_data)
          // this.result(response.data.data_node_add, response.data.data_edge_add)
          this.load()
        })
        .catch(function(error) {
          // console.log(error)
        })
    },
    completeAll() {
      for (var i = 0; i < this.msg.edge_id.length; i++) {
        var aim_link = this.myDiagram.findLinkForKey(this.msg.edge_id[i]).data
        this.myDiagram.model.setDataProperty(aim_link, 'color', 'black')
      }
      for (var j = 0; j < this.msg.node_id.length; j++) {
        var aim_node = this.myDiagram.findNodeForKey(this.msg.node_id[j]).data
        this.myDiagram.model.setDataProperty(aim_node, 'color', 'rgb(0,191,255)')
      }

      console.log(this.text_data)
      // todo: 将数据保存到result文件中
      this.$http
        .post(this.Global_Api + '/api/save_integrity_verification', { total: this.text_data })
        .then(response => {
          console.log(response.data)
          // if (response.data.error_code === 0) {
          //   this.$message({
          //     type: 'success',
          //     message: response.data.result
          //   })
          // }
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    reduction() {
      this.$http
        .get(this.Global_Api + '/api/recovery_origin_model')
        .then(response => {
          console.log(response.data)
          this.reload()
        })
        .catch(function(error) {
          console.log(error)
        })
    },
    saveModel() {
      this.$http
        .get(this.Global_Api + '/api/save_model')
        .then(response => {
          console.log(response.data)
        })
        .catch(function(error) {
          console.log(error)
        })
    }
  }
  // watch: {
  //   msg(newVal, oldVal) {
  //     console.log('新值：' + newVal, '旧值：' + oldVal)
  //     console.log('msg:' + this.msg)
  //   }
  // }
  // computed: {
  //   // 计算属性的 getter
  //   reversedMessage: function() {
  //     // `this` 指向 vm 实例
  //     return this.msg
  //       .split('')
  //       .reverse()
  //       .join('')
  //   }
  // }
}
</script>

<style lang="scss" scoped>
.myDiagramDiv {
  background-color: whitesmoke;
  border: solid 1px black;
  width: 100%;
  height: 480px;
  margin-top: 20px;
  //margin-left: 10%;
}

.text-path {
  text-align: center;
  font-size: x-large;
}

.divHelp {
  margin-left: 1100px;
  height: 40px;
  margin-top: -40px;
  position: absolute;
}
</style>
