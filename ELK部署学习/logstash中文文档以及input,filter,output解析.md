#####  logstash中文文档以及input,filter,output解析

```
input{
	file{
		#注意文件路径名需要绝对路径
		path => "E:/nginx/logs/error.log" 
		#如果想要监听多个目标文件可以改成数组
		path => ["E:/nginx/logs/error.log","E:/nginx/logs/access.log"]
		#排除不想监听的文件(支持字符串或者数组，但是要求必须是绝对路径)
		exclude => "E:/nginx/logs/other.log"
		
		#添加自定义字段
		add_field => {"atack"=>"atack"}
		#增加标签(这个标签可能在后续的处理中起到标志的作用
		tags => "shooter_tag"
		
		#设置新事件标志
		delimiter => "\n"
		
		#设置多长事件扫描目录,发现新文件
		discover_interval => 15
		#设置多长时间检测文件是否被修改
		stat_interval => 1
		
		#监听文件起始位置，beginning 表示【第一次】启动从文件头开始读取，后面动态读取；end表示从文件尾开始（类似tail -f）。
		start_position => beginning 
		
		#sincedb保存每个日志文件已经被读取到的位置,如果Logstash重启,对于同一个文件,会继续从上次记录的位置开始读取。如果想重新从头读取文件,需要删除sincedb文件.如果设置为"/dev/null",即不保存位置信息。
		sincedb_path => "E:\logstash\stat\test.txt"
		#设置多久会写入读取位置信息
		sincedb_write_interval => 15
		
		#编码插件Codec
		#1.如果事件数据是json格式,可以加入codec=>json来进行解析 
		#2.如果你的json文件比较长,需要换行的话,那么就得用到json_lines{}了
		#3.multiline 多行事件有时候有的日志用多行去展现,这么多行其实都是一个事件(比如JAVA的异常日志)  
		codec => multiline {
            pattern => "^\d"
            negate => true
            what => "previous"  #未匹配的内容向前合并
        }
#设置输入规则
        codec2
        codec => multiline {
            #利用正则匹配规则，匹配每一行开始的位置，这里匹配每一行开始的位置为数字
            pattern => "^[0-9]"
     
            #true表示不匹配正则表达式，false为匹配正则表达式，默认false
            #如果不匹配，则会结合what参数，进行合并操作
            negate => true
            
            #what可设置previous和next，previous则表示将所有不匹配的数据都合并到上一个正则事件
            #而next则相反，将所有的不匹配的数据都合并到下一个正则事件
            what => "previous"
 
            #表示当多长时间没有新的数据，最后一个正则匹配积累的多行数据都归属为最后一个事件，这里的10表示10秒
            #auto_flush_interval => 10
       }
 
			
	}
}
filter {
    #在json化之前,使用mutte对\\x字符串进行替换，防止以下错误：ParserError: Unrecognized character escape 'x' (code 120)
    mutate {
        gsub => ["message", "\\x", "\\\x"]
    }
    json {
        source => "message"
        #删除无用字段，节约空间
        remove_field => "message"
        remove_field => "severity"
        remove_field => "pid"
        remove_field => "logsource"
        remove_field => "timestamp"
        remove_field => "facility_label"
        remove_field => "type"
        remove_field => "facility"
        remove_field => "@version"
        remove_field => "priority"
        remove_field => "severity_label"
    }
    date {
        #用nginx请求时间替换logstash生成的时间
        match => ["time_local", "ISO8601"]
        target => "@timestamp"
    }
    grok {
        #从时间中获取day
        match => { "time_local" => "(?<day>.{10})" }
    }
    grok {
        #将request解析成2个字段：method\url
        match => { "request" => "%{WORD:method} (?<url>.* )" }
    }
    grok {
        #截取http_referer问号前的部分，问号后的信息无价值，浪费空间
        match => { "http_referer" => "(?<referer>-|%{URIPROTO}://(?:%{USER}(?::[^@]*)?@)?(?:%{URIHOST})?)" }
    }
    mutate {
        #解析出新的字段后，原字段丢弃
        remove_field => "request"
        remove_field => "http_referer"
		#rename重命名某个字段，如果目的字段已经存在，会被覆盖掉：
        rename => { "http_user_agent" => "agent" }
        rename => { "upstream_response_time" => "response_time" }
        rename => { "host" => "log_source" }
        rename => { "http_x_forwarded_for" => "x_forwarded_for" }
        #以下2个字段以逗号分隔后，以数组形式入库
        split => { "x_forwarded_for" => ", " }
        split => { "response_time" => ", " }
    }
    #alter {
    #    #不满足elasticsearch索引模型的，入库会失败，因此做以下数据转换
    #    condrewrite => [
    #        "x_forwarded_for", "-", "0.0.0.0",
    #        "x_forwarded_for", "unknown", "0.0.0.0",
    #        "response_time", "-", "0",
    #        "real_ip", "", "0.0.0.0"
    #    ]
    #}
}
#(将日志文件按template指定个数输出到nginx_to_logs索引)
output { #入库，以template指定的模型作为索引模型 
    elasticsearch { 
        hosts => ["172.17.0.3:9200"]
		#es要执行的动作 index, delete, create, update
		#1.index:将logstash.时间索引到一个文档
		#2.delete:根据id删除一个document(这个动作需要一个id)
		#3.create:建立一个索引document，如果id存在动作失败.
		#4.update:根据id更新一个document，有一种特殊情况可以upsert--如果document不是已经存在的情况更新document 。参见upsert选项。
		action=>"index"
		
		#为索引提供document id,对重写elasticsearch中相同id词目很有用（但是小心这个id如果重复会让你只能获取到日志的最后一条信息,一般不要设置这个选项,系统会默认随机生成id）
		document_id=> "igshooter"
		
		#事件要被写入的document type,一般要将相似事件写入同一type,可用%{}引用事件type,默认type=log
		#document_type=> ""
		
        index => "nginx_to_logs" #事件要被写进的索引,这里的索引要es已创建，没创建是没用的es也搜不到的
		
        user => elastic
        password => changeme
		
		#一个默认的es mapping 模板将启用（除非设置为false,他就会用自己的template）
        manage_template => true
		
        template_overwrite => true
		#在es内部模板的名字(这个名字可以随意取)
        template_name => "mynginx"
		#有效的filepath 设置自己的template文件路径，不设置就用已有的 (这个文件里的template:索引名称必须和 index设置的索引名称一致，或者包含*)
        template => "/opt/logstash-5.6.4/template/mynginxtemplate.json"
        codec => json #使用codec的json格式输出
		
		#这里需要十分注意的一个问题是,document_id尽量保证值得唯一,这样会解决你面即将面临的ES数据重复问题,切记切记!
    }
    #本地文件放一份，作为ELK的补充
    file {
        flush_interval => 600
        path => '/home/nginxlog/%{day}/%{domain}.log'
        codec => line { format => '<%{time_local}> <%{real_ip}> <%{method}> <%{url}> <%{status}> <%{request_time}> <%{response_time}> <%{body_bytes_sent}> <%{request_body}> <%{referer}> <%{x_f
orwarded_for}> <%{log_source}> <%{agent}>'}
    }
}
```

###### 关于filter过滤

```
1.怎么能把包含SLBHealthCheck字段的日志过滤掉呢？
 
filter {  
    if "SLBHealthCheck" in [message] {  
        drop {}  
    }
}
  
2.如果是多个字段，应该怎么写呢？
 用or 做条件连接 
if "SLBHealthCheck" in [message] or "SLBHealthCheck" in [xxxx] {
 drop{}
}
 
3.删除指定字段
我们可以通过filter删除指定字段.
filter {
  drop {
    remove_field => [ “foo_%{somefield}” ]
  }
}
4.也可以增加字段.
filter {
  drop {
    add_field => { “foo_%{somefield}” => “Hello world, from %{host}” }
  }
}
```













[ELK中文指南]: https://elkguide.elasticsearch.cn/kibana/v5/plugin/server-develop.html



