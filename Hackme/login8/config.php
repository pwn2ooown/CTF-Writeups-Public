<code><span style="color: #000000">
<span style="color: #0000BB">&lt;?php<br />define</span><span style="color: #007700">(</span><span style="color: #DD0000">'ROOT'</span><span style="color: #007700">,&nbsp;</span><span style="color: #0000BB">dirname</span><span style="color: #007700">(</span><span style="color: #0000BB">realpath</span><span style="color: #007700">(</span><span style="color: #0000BB">__FILE__</span><span style="color: #007700">)));<br /></span><span style="color: #0000BB">define</span><span style="color: #007700">(</span><span style="color: #DD0000">'DEBUG_MODE'</span><span style="color: #007700">,&nbsp;</span><span style="color: #0000BB">false</span><span style="color: #007700">);<br /><br /></span><span style="color: #0000BB">$flag&nbsp;</span><span style="color: #007700">=&nbsp;</span><span style="color: #DD0000">"FLAG{object&nbsp;injection&nbsp;G____G}"</span><span style="color: #007700">;<br /></span><span style="color: #FF8000">//&nbsp;hidden&nbsp;flag:&nbsp;"FLAG{wake&nbsp;up&nbsp;neo}";<br /><br /></span><span style="color: #0000BB">$users&nbsp;</span><span style="color: #007700">=&nbsp;[<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'guest'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;[<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'password'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;</span><span style="color: #DD0000">'guest'</span><span style="color: #007700">,<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'admin'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;</span><span style="color: #0000BB">false</span><span style="color: #007700">,<br />&nbsp;&nbsp;&nbsp;&nbsp;],<br />&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'admin'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;[<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'password'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;</span><span style="color: #0000BB">false</span><span style="color: #007700">,&nbsp;</span><span style="color: #FF8000">//&nbsp;admin&nbsp;account&nbsp;disabled<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color: #DD0000">'admin'&nbsp;</span><span style="color: #007700">=&gt;&nbsp;</span><span style="color: #0000BB">true</span><span style="color: #007700">,<br />&nbsp;&nbsp;&nbsp;&nbsp;],<br />];<br /></span>
</span>
</code>
