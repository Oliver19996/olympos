import 'package:flutter/material.dart';
import 'api.dart';

void main() => runApp(const OlymposApp());

class OlymposApp extends StatelessWidget {
  const OlymposApp({super.key});
  @override
  Widget build(BuildContext context) => MaterialApp(
        debugShowCheckedModeBanner: false,
        theme: ThemeData.dark().copyWith(
          scaffoldBackgroundColor: const Color(0xFF0B0A0D),
          colorScheme: const ColorScheme.dark(
            primary: Color(0xFFD12B5B), secondary: Color(0xFFC8A96B),
            surface: Color(0xFF17131A)),
          useMaterial3: true,
        ),
        home: const HomePage(),
      );
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override State<HomePage> createState() => _HomePageState();
}
class _HomePageState extends State<HomePage> {
  int index=0; final api=OlymposApi();
  @override Widget build(BuildContext context){
    final pages=[const ConceptPage(),JoinPage(api:api),DashboardPage(api:api)];
    return Scaffold(appBar:AppBar(title:const Text('OLYMPOS',style:TextStyle(fontFamily:'serif',letterSpacing:4)),actions:[Padding(padding:const EdgeInsets.all(12),child:Chip(label:const Text('Phase 0')))]),body:pages[index],bottomNavigationBar:NavigationBar(selectedIndex:index,onDestinationSelected:(i)=>setState(()=>index=i),destinations:const [NavigationDestination(icon:Icon(Icons.auto_awesome),label:'概要'),NavigationDestination(icon:Icon(Icons.person_add),label:'登録'),NavigationDestination(icon:Icon(Icons.insights),label:'KPI')]));
  }
}

class ConceptPage extends StatelessWidget {
  const ConceptPage({super.key});
  @override Widget build(BuildContext context)=>ListView(padding:const EdgeInsets.all(24),children:[
    const SizedBox(height:40),
    Text('最大7名から、\nひとりを選ぶ。',style:Theme.of(context).textTheme.displaySmall?.copyWith(fontFamily:'serif',fontWeight:FontWeight.bold)),
    const SizedBox(height:16),
    const Text('無限にスワイプするアプリではありません。主役1名と共演者最大7名が同じクールに入り、2週間でひとりを選びます。',style:TextStyle(color:Color(0xFFB9AFB4),height:1.7)),
    const SizedBox(height:24),
    const _Card(title:'ZEUS',body:'男性主役1名と、女性共演者6〜7名。主役が物語の中心です。'),
    const _Card(title:'APHRODITE',body:'女性主役1名と、男性共演者6〜7名。ルールはZEUSと同じです。'),
    const SizedBox(height:20),
    Text('ほかのアプリと、ここが違う',style:Theme.of(context).textTheme.titleMedium?.copyWith(color:const Color(0xFFC8A96B),fontWeight:FontWeight.bold)),
    const SizedBox(height:8),
    const _Card(title:'終わりがある',body:'同時に何人も話さない。1クールは最大7名、2週間で決着。'),
    const _Card(title:'絞って、双方で決める',body:'7名→4名→2名。最後は双方投票。一方的な「いいね」では成立しない。'),
    const _Card(title:'共演者同士は実写を見ない',body:'共演者同士はAI似顔絵。実写は主役との間だけ。氏名も電話も最初は出さない。'),
    const SizedBox(height:12),
    const Card(child:Padding(padding:EdgeInsets.all(16),child:Text('検証版では課金・eKYC・実デートを行いません。'))),
  ]);
}
class _Card extends StatelessWidget {const _Card({required this.title,required this.body});final String title,body;@override Widget build(BuildContext c)=>Card(child:ListTile(title:Text(title,style:const TextStyle(color:Color(0xFFC8A96B),fontWeight:FontWeight.bold)),subtitle:Text(body)));}

class JoinPage extends StatefulWidget {const JoinPage({super.key,required this.api});final OlymposApi api;@override State<JoinPage> createState()=>_JoinPageState();}
class _JoinPageState extends State<JoinPage>{String gender='male',role='host',age='25-29',message='';bool portrait=false,busy=false;Future<void> submit()async{setState(()=>busy=true);try{final id=await widget.api.register(gender:gender,target:gender=='male'?'female':'male',role:role,ageBand:age,portraitOptIn:portrait);setState(()=>message='匿名ID: $id');}catch(e){setState(()=>message='API接続エラー: $e');}finally{setState(()=>busy=false);}}@override Widget build(BuildContext c)=>ListView(padding:const EdgeInsets.all(20),children:[Text('匿名プロフィール',style:Theme.of(c).textTheme.headlineMedium),DropdownButtonFormField(value:gender,items:const [DropdownMenuItem(value:'male',child:Text('男性')),DropdownMenuItem(value:'female',child:Text('女性'))],onChanged:(v)=>setState(()=>gender=v!)),DropdownButtonFormField(value:role,items:const [DropdownMenuItem(value:'host',child:Text('主役')),DropdownMenuItem(value:'candidate',child:Text('共演者'))],onChanged:(v)=>setState(()=>role=v!)),DropdownButtonFormField(value:age,items:['20-24','25-29','30-34','35-39'].map((x)=>DropdownMenuItem(value:x,child:Text(x))).toList(),onChanged:(v)=>setState(()=>age=v!)),SwitchListTile(value:portrait,onChanged:(v)=>setState(()=>portrait=v),title:const Text('AIによる似顔絵をマッチングアプリに使うことに賛成')),FilledButton(onPressed:busy?null:submit,child:Text(busy?'登録中…':'同意して匿名登録')),SelectableText(message)]);}

class DashboardPage extends StatefulWidget{const DashboardPage({super.key,required this.api});final OlymposApi api;@override State<DashboardPage> createState()=>_DashboardPageState();}
class _DashboardPageState extends State<DashboardPage>{Map<String,dynamic>? data;String error='';Future<void> load()async{try{await widget.api.simulate();final d=await widget.api.kpis();setState(()=>data=d);}catch(e){setState(()=>error='$e');}}@override Widget build(BuildContext c)=>ListView(padding:const EdgeInsets.all(20),children:[Text('検証KPI',style:Theme.of(c).textTheme.headlineMedium),FilledButton(onPressed:load,child:const Text('匿名編成を実行')),if(error.isNotEmpty)Text(error),if(data!=null)...['participation_intent_rate','payment_intent_rate','portrait_approval_rate','formation_rate'].map((k)=>Card(child:ListTile(title:Text(k),trailing:Text('${((data![k]??0)*100).round()}%'))))]);}
