-- Adapta la nota de Obsidian al PIF: sin portada/indice manual, capitulos con caratula.
local function caratula(t)
  return pandoc.RawBlock("latex",
    "\\clearpage\\thispagestyle{empty}\\vspace*{\\fill}\n" ..
    "{\\centering\\bfseries\\Large " .. t .. "\\par}\n" ..
    "\\vspace*{\\fill}\\clearpage\n" ..
    "\\addcontentsline{toc}{chapter}{" .. t .. "}")
end

function Pandoc(doc)
  local out, started, skip = {}, false, false
  for _, b in ipairs(doc.blocks) do
    local text = pandoc.utils.stringify(b)
    if b.t == "Header" and b.level == 1 and text:match("^Resumen") then started = true end
    if b.t == "Para" and text:match("^Índice") then skip = true end
    if b.t == "Header" and text:match("^CAPÍTULO I ") then skip = false end
    if started and not skip and not (b.t == "Header" and text == "") then
      if b.t == "Header" and b.level == 1 and text:match("^CAPÍTULO") then
        out[#out + 1] = caratula((text:gsub("[#%%&_{}]", "\\%0")))
      else
        out[#out + 1] = b
      end
    end
  end
  doc.blocks = out
  return doc
end

function Link(l) if l.classes:includes("wikilink") then return l.content end end
function Str(s) if s.text:find("↩", 1, true) then return pandoc.Str((s.text:gsub("↩", ""))) end end
