<!-- This is to make the GitHub Page for the repo look nice  -->

{%- capture link_icon -%}
<svg viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg>
{%- endcapture -%}
{% capture conventions %}{% include_relative Coding-Conventions.md %}{% endcapture %}
{% assign conventions2 = conventions | newline_to_br | split: "<br />" %}

{% assign auto_id = false %}
{% assign code_block = false %}

{% for line in conventions2 %}
{%- if line contains "<!-- Begin Auto-ID -->" -%}
{%- assign auto_id = true -%}
{%- endif -%}

    {%- assign first_token = line | split: " " | first -%}
    {%- if first_token contains "```" -%}
        {%- if code_block -%}{%- assign code_block = false -%}
        {%- else -%}{%- assign code_block = true -%}
        {%- endif -%}
    {%- endif -%}

    {%- assign first_token_char = first_token | slice: 0 -%}
    {%- if auto_id and first_token_char == "#" and code_block == false -%}
        {% comment %}Omit hyphens, as we need the whitespace to denote a header{% endcomment %}
        {% assign header_text = line | split: first_token | last %}
        {% assign header_id = line | split: "]" | first | split: "[" | last | replace: ".","_" | downcase %}

{{ first_token }} [{{link_icon}}](#{{header_id}}) {{ header_text }} {#{{ header_id }}}
{%- else -%}
{{ line }}
{%- endif -%}
{%- if line contains "<!-- TOC -->" -%}

- TOC
  {:toc}
  {%- endif -%}
  {% endfor %}

<style>
#markdown-toc svg {
    display: none;
}
</style>
