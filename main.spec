# -*- mode: python -*-

block_cipher = None

needed_selenium_files = [
                        ('C:/Users/itaraday/Anaconda3/envs/py2.7/Lib/site-packages/selenium/webdriver/firefox/webdriver_prefs.json','DATA'),
                        ('C:/Users/itaraday/Anaconda3/envs/py2.7/Lib/site-packages/selenium/webdriver/firefox/webdriver.xpi', 'DATA')
                        ]
                           
a = Analysis(['main.py'],
             pathex=['C:/Users/itaraday/My Documents/python/SBLocations'],
             binaries= None,
             datas=needed_selenium_files,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=['boto'],
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
             
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
             
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='SBLocationatorBot',
          debug=False,
          strip=None,
          upx=True,
          console=True )
