# -*- mode: python -*-

block_cipher = None


a = Analysis(['CBPlotter.py'],
             pathex=['C:\\Users\\Administrator\\Documents\\plotter backup\\Plotter_Ver1.1'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CBPlotter',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='p2mpIcon-2.ico')
