-- installer for getnonfreefonts
--
-- (c) 2010-2023 Reinhard Kotucha
--
-- This work is licensed under the 'LaTeX Project Public License',
-- either version 1.3c of the license, or (at your option) any later
-- version.  See
--
--   http://www.latex-project.org/lppl.txt
--
-- for details.
--
-- ------------------------------------------------------------------
--
-- This is a TeX-Lua script.  It should be run with the texlua executable.
--
--   texlua install-getnonfreefonts.sh
--
-- It can be used to install the getnonfreefonts scripts into the TeX
-- directory structure and to create the necessary links or wrapper
-- scripts.
--
-- See the manual of getnonfreefonts for more details.

local name, version = "install-getnonfreefonts", "1.6"

local function basename (str)
  return str:gsub("(.*/)(.*)", "%2")
end

kpse.set_program_name(basename(arg[0]))

local kpse_err = io.popen("kpsewhich --version")
if not kpse_err then
  print(kpse.progname .. ": kpsewhich utility not found.")
  print("Are the TeX utilities in the search path?")
  os.exit(1)
end
kpse_err:close()

-- platform settings

local os_id, os_release = os.identify()

-- is the script run with admin privileges?

local is_admin = false
if os_id == "windows" then
  local test_admin = io.popen("net session >nul 2>&1")
  local status, msg = test_admin:close()
  -- the command 'net session' is only available for admins,
  -- so if msg is 'exit' and status is true, we have admin rights.
  if status and msg == 'exit' then
    is_admin = true
  end
else -- unix, os2
  -- we rely on the POSIX function 'geteuid'.
  -- But as there is no FFI library installed by default in TeX Live
  -- we call an external command.
  local test_admin = io.popen("id -u")
  local euid = test_admin:read("*n")
  if euid == 0 then
    is_admin = true
  end
  test_admin:close()
end

local function get_texmf_root (var)
  local texmf_root = kpse.var_value(var)
  if not texmf_root then
    print(kpse.progname .. ": Can't determine " .. var .. ".")
    print("Maybe the permissions are wrong.")
    os.exit(1)
  end
  return texmf_root
end

-- TeX Live, teTeX and fpTeX
local texmf_dist = get_texmf_root("TEXMFDIST")
local texmf_main = get_texmf_root("TEXMFMAIN")
local texmf_local = get_texmf_root("TEXMFLOCAL")

-- MikTeX
if not texmf_dist then
  texmf_dist = get_texmf_root("TEXMF")
  texmf_main = texmf_dist
  texmf_local = get_texmf_root("CommonConfig") .. "/miktex/texmfs/install"
end

local dest_dir

if is_admin then
  dest_dir = texmf_main
else
  dest_dir = kpse.var_value("TEXMFHOME")
  if not dest_dir or dest_dir == "" then
    print(kpse.progname .. ": Variable TEXMFHOME not set.")
    os.exit(1)
  end
end

print("Installing for " .. os_id .. "...")
if is_admin then
  print("Installing in system-wide directory: " .. dest_dir)
else
  print("Installing in user directory: " .. dest_dir)
end

-- create destination directories

local scripts_dir = dest_dir .. "/scripts/getnonfreefonts"
local doc_dir     = dest_dir .. "/doc/support/getnonfreefonts"
local man_dir     = dest_dir .. "/doc/man/man1"
local bin_dir

if os_id == "windows" then
  bin_dir = dest_dir .. "/scripts/texlive"
else -- unix, os2
  if is_admin then
    -- TeX Live, fpTeX
    local texmf_var = get_texmf_root("TEXMFVAR")
    local texmf_sys_var = kpse.var_value("TEXMFSYSVAR") or texmf_var
    bin_dir = texmf_sys_var:gsub("texmf%-var", "bin")
    -- teTeX
    bin_dir = bin_dir or texmf_dist:gsub("texmf-dist", "bin")
    if not lfs.attributes(bin_dir, "mode") then
      -- MacTeX
      bin_dir = texmf_dist:gsub("/texmf%-dist", "/bin")
      local arch = io.popen("uname -m"):read("*l")
      if arch then
        bin_dir = bin_dir .. "/" .. arch .. "-darwin"
      end
    end
  else -- no admin
    bin_dir = os.getenv("HOME") .. "/bin"
  end
end

-- create directories

local dirs = { scripts_dir, doc_dir, bin_dir }
if os_id ~= "windows" then
  dirs[#dirs+1] = man_dir
end

for i=1, #dirs do
  local d = dirs[i]
  if d and not lfs.attributes(d, "mode") then
    print("Creating directory " .. d .. "...")
    assert(lfs.mkdir(d))
  end
end

-- url of the repository

local url = "http://tug.org/fonts/getnonfreefonts/"

-- download and install files

local scripts = {
  "getnonfreefonts",
  "getfont.pl",
  "special.map"
}

local docs = {
  "getnonfreefonts.html",
  "getnonfreefonts.pdf",
  "getnonfreefonts-ja.html",
  "getnonfreefonts-ja.pdf",
  "getnonfreefonts.txt",
  "README"
}

local man_pages = {
  "getnonfreefonts.1"
}

-- download files

print("Downloading files from " .. url .. "...")

local tmp_dir = assert(lfs.tmpdir()) .. "/getnonfreefonts"
assert(lfs.mkdir(tmp_dir))

local all_files = {}
for i=1, #scripts do
  all_files[#all_files+1] = scripts[i]
end
for i=1, #docs do
  all_files[#all_files+1] = docs[i]
end
if os_id ~= "windows" then
  for i=1, #man_pages do
    all_files[#all_files+1] = man_pages[i]
  end
end

for i=1, #all_files do
  local f = all_files[i]
  print("  -> " .. f)
  local dest_file = tmp_dir .. "/" .. f
  local get_file = io.popen("curl -L -s -o ".. dest_file .. " " .. url .. f)
  get_file:close()
end

-- install files

print("Installing files in " .. dest_dir .. "...")

for i=1, #scripts do
  local s = scripts[i]
  print("  -> " .. s)
  os.copyfile(tmp_dir .. "/" .. s, scripts_dir .. "/" .. s)
end
for i=1, #docs do
  local d = docs[i]
  print("  -> " .. d)
  os.copyfile(tmp_dir .. "/" .. d, doc_dir .. "/" .. d)
end
if os_id ~= "windows" then
  for i=1, #man_pages do
    local m = man_pages[i]
    print("  -> " .. m)
    os.copyfile(tmp_dir .. "/" .. m, man_dir .. "/" .. m)
  end
end

-- make scripts executable

if os_id ~= "windows" then
  for i=1, #scripts do
    local s = scripts[i]
    lfs.chmod(scripts_dir .. "/" .. s, "a+x")
  end
end

-- create wrappers or symlinks

print("Creating wrappers or symlinks in " .. bin_dir)

for i=1, #scripts do
  local s = scripts[i]
  local wrapper = bin_dir .. "/" .. s
  if os_id == "windows" then
    wrapper = wrapper .. ".exe"
    local kpse_run = assert(io.popen("kpsewhich runscript.exe"))
    local runscript = kpse_run:read("*l")
    kpse_run:close()
    -- TeX Live, fpTeX
    if runscript then
      os.copyfile(runscript, wrapper)
    else
      -- MiKTeX
      local kpse_miktex = assert(io.popen("kpsewhich miktex-luatex.exe"))
      local luatex = kpse_miktex:read("*l")
      kpse_miktex:close()
      os.copyfile(luatex, wrapper)
    end
  else -- unix, os2
    lfs.symlink(scripts_dir .. "/" .. s, wrapper)
  end
end

-- remove temporary directory

assert(lfs.rmdir(tmp_dir))

print("Done.")