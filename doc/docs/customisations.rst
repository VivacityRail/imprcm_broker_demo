:orphan:

Customisations
==============

These are some ways to customise the text layout (see guide in http://ryan-roemer.github.io/sphinx-bootstrap-theme/examples.html). 

The colours and text formats can be set by applying overrides in the `Stylesheet <\_static/imp_rcm_overrides.css>`_

.. note:: This is a **note**.
   It can be quite a lot longer and extend over several lines.

.. todo:: This is a **todo** item.
   And this text describes what needs to be done.  Note that you can strike out elements of the todo if they've been fixed using markup like this:

   :strike:`a very important task that had to be done`.

.. warning:: This is a **warning**.

.. danger:: This shows that there is **danger**.

.. tip:: This a **tip**.

.. attention:: This demands your **attention**.

.. important:: This is rather **important**.

.. error:: This is definitely an **error**.

A "**bordered**" grid table:

.. cssclass:: table-bordered

+------------------------+------------+----------+----------+
| Header1                | Header2    | Header3  | Header4  |
+========================+============+==========+==========+
| row1, cell1            | cell2      | cell3    | cell4    |
+------------------------+------------+----------+----------+
| row2 ...               | ...        | ...      |          |
+------------------------+------------+----------+----------+
| ...                    | ...        | ...      |          |
+------------------------+------------+----------+----------+

A simple "**striped**" table:

.. cssclass:: table-striped


+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|Objectives                         |Overall aims. Aims may be different according to party.                                               |x|                                                                                                                                                                                                                                                                                               |PB / DS                           |Preamble              |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Common endeavour or risk / reward mechanism involved?                                                 |x|VRC: we don't believe a formal risk/reward arrangement is on the cards here, but you may use this heading to agree basic arrangements for sharing of cost and benefit.                                                                                                                         |                                  |Preamble              |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|Parties inc governance             |Identify roles including scheme lead / promoter                                                       |x|T1010-02 lists these roles: Scheme Lead / Joint Scheme Leads; Suppliers (of equipment / software / installation / maintenance); Data Collectors, Hosters, Processors, Analysts, Distributors; Data Receivers / Users / Beneficiaries; Scheme facilitators.                                     |                                  |n/a                   |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Hardware / software suppliers, installers, maintainers                                                |x|                                                                                                                                                                                                                                                                                               |                                  |n/a                   |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Data collectors, processors and users                                                                 |x|                                                                                                                                                                                                                                                                                               |                                  |n/a                   |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Scheme facilitators                                                                                   |x|                                                                                                                                                                                                                                                                                               |                                  |n/a                   |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Agree governance group meetings                                                                       | |                                                                                                                                                                                                                                                                                               |                                  |Schedule 8            |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+
|                                   |Agree programme management - monitoring, risks, issues, decisions                                     | |                                                                                                                                                                                                                                                                                               |                                  |Schedule 8            |
+-----------------------------------+------------------------------------------------------------------------------------------------------+-+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+----------------------+




=====  =====  =======
H1     H2     H3
=====  =====  =======
cell1  cell2  cell3
...    ...    ...
...    ...    ...
=====  =====  =======

which uses the directive::

    .. cssclass:: table-striped

And a "**hoverable**" table:

.. cssclass:: table-hover

=====  =====  =======
H1     H2     H3
=====  =====  =======
cell1  cell2  cell3
...    ...    ...
...    ...    ...
=====  =====  =======

which uses the directive::

    .. cssclass:: table-hover


Links into T1010
----------------

Link to whole T1010 document: `Process Map Top Level <\_static/T1010/T1010-02/Appendix\_C2\_RCM\_process\_map.pdf>`_


Note format of link: ```Process Map Top Level <\_static/T1010/T1010-02/Appendix\_C2\_RCM\_process\_map.pdf>`_``
 * quotes are backticks
 * following underscore
 * internal underscores must be escaped with \\
 * opens in existing window

Link to page in T1010 document: `Process Map Detail A <\_static/T1010/T1010-02/Appendix\_C2\_RCM\_process\_map.pdf#page=2>`_


Note format of link:
 * ``#page=n`` on the end of link, where n is page number
 
To get links to open in a new tab or window, it is probably best to use Ctrl-click (for new tab) or Shift-click (for new window). However, 
it is possible to force it by using a ``.. raw::`` directive and the ``target="_blank"`` option.

Link to page opens in new tab: |link_in_new_tab|

.. |link_in_new_tab| raw:: html

   <a href="_static/T1010/T1010-02/Appendix_C2_RCM_process_map.pdf#page=3" target="_blank">Process Map Detail B</a>


Note format of link:
 * use of intermediate link in bars ``|like_this|``. These must be unique.
 * no need to escape underscores in the raw html.
 
Sidebar
-------

This defines a sidebar using the ``.. sidebar::`` directive

.. sidebar:: Test Sidebar
   :subtitle: What a wonderful extra bit of information!
   
   This is what goes into the sidebar. It can be pretty much **any
   text**.
   
The sidebar probably shouldn't be too close to a topic as it looks like they tend to overlap.

So it's a good idea to use one or the other but not both.
   
Topic
-----

This defines a topic using the ``.. topic::`` directive

.. topic:: Here's a useful snippet of extra information
   
   A topic is a separate bit of text that is highlighted to separate it from the document flow.
   This is more text in the topic.
   
   
More stuff
----------

There could be more down here.


See Also
--------

You can add a "see also" block using the ``.. seealso::`` directive.

.. seealso:: 

   `Process Map Top Level <\_static/T1010/T1010-02/Appendix\_C2\_RCM\_process\_map.pdf>`_
      T1010-02 process map.

Other directives
----------------

The ``.. highlights::`` directive

.. highlights::
  This is a section like a topic whose original purpose was to indicate the bullet points that the paragraph below contains. We can use it as a generic callout like a topic
  
  * First key point

  * Second key point
  
  * Third key point

The ``.. epigraph::`` directive
  
.. epigraph::
  This is the epigraph text which appears at the top of a section. Its original purpose is to allow space for a pompous, humorous or apposite quote from some worthy like Mark Twain or Sun Tzu.

.. rubric::
  This is a rubric

	  
Glossary
--------

You can add a glossary using the ``.. glossary::`` directive.  Example below. You can then refer to items in the glossary using a 
``:term:`` element.  So here is :term:`XIRCMSG` referred to.  The glossary can be automatically sorted using the ``:sorted:`` flag so you don't need to bother doing it.

.. glossary::
   :sorted: 

   XIRCMSG
      Cross-industry remote condition monitoring strategy group

   RSSB
      Rail Safety and Standards board
	
To-Do List
--------------
We can include a list  of all the todo items (tagged ``.. todo:: xxx`` using ``.. todolist::``.

To make it appear, we need to set the config option ``todo_include_todos`` to ``True`` in ``conf.py``.

.. todolist:: 

Work in Progress
-----------------
You can format a section to show it's work in progress by putting a ``.. cssclass:: imprcm-wip`` directive above the section heading.

.. cssclass:: imprcm-wip

WIP section
~~~~~~~~~~~

This section of text is still work in progress. It's got a ``.. cssclass:: imprcm-wip`` directive just above it. 

So you should treat it as provisional for now.

This bit hasn't been finished yet either.
   
Finished Section
----------------
This is all done and dusted so renders normally.  If there's just a paragraph that's WIP, you can use a ``.. container:: imprcm-wip`` directive to wrap the text.

.. container:: imprcm-wip

   This is a wip sentence

This is all fantastic.

.. cssclass:: imprcm-wip

Another WIP Section
-------------------
This is still under construction ...

Another Finished section
------------------------

but this is finished.



Including pictures
---------------------

Pictures are included using a ``.. image:: path/to/my/image_file.jpg`` tag. The path would normally be ``_static/images/<page_name_no_extension>/filename``. You can add extra info such as ``:height``, ``:width``, ``:alt`` and justification such as ``:left`` (which means text will flow around the picture)

SVG files
~~~~~~~~~

Most pictures would be normal .jpg or .png files. Some more useful stuff can be done using .svg files (which can handily be created from LucidChart). The original diagram from which the SVG files in this example are made has links to other documentation pages associated with the boxes.

Static svg. Links associated with the boxes don't work.

.. image:: _static/images/index/Embed_test2.svg
   :alt: Basic image

svg embedded as object . The boxes are clickable links to other pages.  


.. note:: the SVG from LucidChart has been doctored by adding ``style="cursor:pointer"`` to the <a> items containing the xref links to other pages.
  
.. raw:: html   

   <object style="width:480px;" data="_static/images/index/Embed_test2.svg" type="image/svg+xml"></object>

.. <div style="width: 480px; margin: 10px; position: relative;"><object style="width:480px;" data="_static/images/index/Embed_test2.svg" type="image/svg+xml"></object></div>

This is an svg included as raw inline html in a ``.. raw:: html`` tag. The hover styling comes from the stylesheet. The boxes have links to other pages associated with them.

.. raw:: html

   <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:lucid="lucid" width="480" height="160"><g transform="translate(-140 -200)" lucid:page-tab-id="0_0"><path d="M0 0h1870.4v1323.2H0z" fill="#fff"/><a href="/investigate.html" target="_top"><path d="M160 220h160v120H160z" stroke="#000" stroke-opacity="0" stroke-width=".5" fill="#141b4d"/><use xlink:href="#a" transform="matrix(1,0,0,1,165,225) translate(22.88888888888888 59)"/><path class="lucid-link lucid-hotspot lucid-overlay-hotspot" d="M160 220h160v120H160z" fill="none"/></a><a href="/technical.html" target="_top"><path d="M440 220h160v120H440z" stroke="#000" stroke-opacity="0" stroke-width=".5" fill="#7fc31c"/><use xlink:href="#b" transform="matrix(1,0,0,1,445,225) translate(29.72222222222222 59)"/><path class="lucid-link lucid-hotspot lucid-overlay-hotspot" d="M440 220h160v120H440z" fill="none"/></a><path d="M320 280h101.76" stroke="#000" stroke-width="2" fill="none"/><path/><path d="M436.76 280l-14.26 4.64v-9.28z"/><path d="M440 280l-18.5 6v-12zm-16.5 3.26l10.03-3.26-10.03-3.26z"/><defs><path fill="#fff" d="M24 0v-248h52V0H24" id="c"/><path fill="#fff" d="M135-194c87-1 58 113 63 194h-50c-7-57 23-157-34-157-59 0-34 97-39 157H25l-1-190h47c2 12-1 28 3 38 12-26 28-41 61-42" id="d"/><path fill="#fff" d="M128 0H69L1-190h53L99-40l48-150h52" id="e"/><path fill="#fff" d="M185-48c-13 30-37 53-82 52C43 2 14-33 14-96s30-98 90-98c62 0 83 45 84 108H66c0 31 8 55 39 56 18 0 30-7 34-22zm-45-69c5-46-57-63-70-21-2 6-4 13-4 21h74" id="f"/><path fill="#fff" d="M137-138c1-29-70-34-71-4 15 46 118 7 119 86 1 83-164 76-172 9l43-7c4 19 20 25 44 25 33 8 57-30 24-41C81-84 22-81 20-136c-2-80 154-74 161-7" id="g"/><path fill="#fff" d="M115-3C79 11 28 4 28-45v-112H4v-33h27l15-45h31v45h36v33H77v99c-1 23 16 31 38 25v30" id="h"/><path fill="#fff" d="M25-224v-37h50v37H25zM25 0v-190h50V0H25" id="i"/><path fill="#fff" d="M195-6C206 82 75 100 31 46c-4-6-6-13-8-21l49-6c3 16 16 24 34 25 40 0 42-37 40-79-11 22-30 35-61 35-53 0-70-43-70-97 0-56 18-96 73-97 30 0 46 14 59 34l2-30h47zm-90-29c32 0 41-27 41-63 0-35-9-62-40-62-32 0-39 29-40 63 0 36 9 62 39 62" id="j"/><path fill="#fff" d="M133-34C117-15 103 5 69 4 32 3 11-16 11-54c-1-60 55-63 116-61 1-26-3-47-28-47-18 1-26 9-28 27l-52-2c7-38 36-58 82-57s74 22 75 68l1 82c-1 14 12 18 25 15v27c-30 8-71 5-69-32zm-48 3c29 0 43-24 42-57-32 0-66-3-65 30 0 17 8 27 23 27" id="k"/><g id="a"><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,0,0)" xlink:href="#c"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,5.555555555555555,0)" xlink:href="#d"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,17.72222222222222,0)" xlink:href="#e"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,28.833333333333332,0)" xlink:href="#f"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,39.94444444444444,0)" xlink:href="#g"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,51.05555555555556,0)" xlink:href="#h"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,57.66666666666668,0)" xlink:href="#i"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,63.22222222222223,0)" xlink:href="#j"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,75.3888888888889,0)" xlink:href="#k"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,86.50000000000001,0)" xlink:href="#h"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,93.11111111111113,0)" xlink:href="#f"/></g><path fill="#fff" d="M136-208V0H84v-208H4v-40h212v40h-80" id="l"/><path fill="#fff" d="M190-63c-7 42-38 67-86 67-59 0-84-38-90-98-12-110 154-137 174-36l-49 2c-2-19-15-32-35-32-30 0-35 28-38 64-6 74 65 87 74 30" id="m"/><path fill="#fff" d="M114-157C55-157 80-60 75 0H25v-261h50l-1 109c12-26 28-41 61-42 86-1 58 113 63 194h-50c-7-57 23-157-34-157" id="n"/><path fill="#fff" d="M25 0v-261h50V0H25" id="o"/><g id="b"><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,0,0)" xlink:href="#l"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,10.666666666666666,0)" xlink:href="#f"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,21.77777777777778,0)" xlink:href="#m"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,32.888888888888886,0)" xlink:href="#n"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,45.05555555555555,0)" xlink:href="#d"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,57.22222222222222,0)" xlink:href="#i"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,62.77777777777777,0)" xlink:href="#m"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,73.88888888888889,0)" xlink:href="#k"/><use transform="matrix(0.05555555555555555,0,0,0.05555555555555555,85,0)" xlink:href="#o"/></g></defs></g></svg>


Scaling SVGs
~~~~~~~~~~~~

The SVGs generated by Lucidchart are the size they were drawn. To scale them to fit to a specific size (say, max width 640px), you need to adjust the top-level ``<g>`` element. The trick is:

- note down the width and height of the SVG (so, for the example above, ``width="480" height="160"``).
- from the proportions of the image, work out what its height would need to be for the width you want (e.g. 640 / 480 x 160 = 213)
- add a viewbox attribute that has the original width and height in it: ``viewbox="0 0 480 160"``
- correct the image width and height to the values you need - desired width and calculated height for example (``width="640" height="213"``).

It will probably be possible to automate this process using powershell.
  
Embedded LucidChart material
~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
   
Live lucidchart. The boxes should be clickable in this one and link to target pages. The image can also be edited in LucidChart. It's a ``.. raw:: html`` tag with a LucidChart-provided embed link.

.. raw:: html

  <div style="width: 640px; height: 480px; margin: 10px; position: relative;"><iframe allowfullscreen frameborder="0" style="width:640px; height:480px" src="https://www.lucidchart.com/documents/embeddedchart/77f7f80a-579e-482a-93f5-ce64da6421c2" id="Qvo6fNy9v-Tw"></iframe></div>


Lucidchart link to selected bit of diagram. This is live so if the diagram changes, the picture will too (though you may need to do ctrl-F5 to refresh the browser cache to see the changes). However, it doesn't include page links. This is a normal ``.. image::`` tag with Lucidchart-provided link.

.. image:: https://www.lucidchart.com/publicSegments/view/7ecb8f58-de74-48d9-b182-97df431104bc/image.png  
   :alt: published lucidchart snip


Embedded big LucidChart diagram. See what happens when you click the **Very important box**.  This is a LucidChart embed, but with actions attached to show / hide layers.

.. raw:: html

   <div style="width: 640px; height: 480px; margin: 10px; position: relative;"><iframe allowfullscreen frameborder="0" style="width:640px; height:480px" src="https://www.lucidchart.com/documents/embeddedchart/77f7f80a-579e-482a-93f5-ce64da6421c2" id="QxCOVKCajcZF"></iframe></div>   



Test of Swagger integration
===========================

This should include a swagger / openapi spec at this point:

.. openapi:: _openapi/swagger.yaml

	
