<h1 align="center">ThemeForge</h1>
<p align="center">Theme Compiler for Android-Based Operating Systems</p>


## Usage

```
ThemeForge [-h] [-b OUTPUT FILE PATH] [-u SOURCE FILE PATH] PATH
```

- **PATH**
  - path to **forge.json** *(will use existing config)* or directory *(will initialize new workspace)*

- **`-b, --build FILE PATH`**
  - build and compile theme to specified file path

- **`-u, --unpack FILE PATH`**
  - unpack a compiled theme from specified file path


### Package Configuration

The application builds and unpacks theme packages based on the configuration inside the **forge.json** file, which is created whenever it is initialized.

```json
{
   "workspace": {
      "build": "build",
      "working": "theme",
      "temp": ".temp"
   },
   "engine": {
      "zip": [
         "com.android.*",
         "com.bbm.*",
         "com.vivo.*",
         "com.huawei.*",
         "framework-*",
         "com.bbk.*"
      ],
      "ignore": [
         ".*"
      ],
      "compression": {
         "method": "default",
         "command": "7z a -tzip -m0=lzma -mx=9 {dest} {src}"
      }
   }
}
```


### Workspace Settings

Each node represents a directory that the application uses. All values must be absolute or relative to the directory containing the **forge.json** file.


### Engine Settings

- **`zip`**
  - folders that match this pattern are compressed to zip format
  
- **`ignore`**
  - files and folders that match this pattern are not included in the theme package
  
- **`compression`**
  - method to be used when compressing files, changing **`"method": "command"`** will execute the defined value in **command** key. `dest` and `src` will be automatically replaced.


## Running from Source

> **NOTE:** 
> This script uses the **Python 3.7** ZipFile library which supports compression levels.


- Clone or download the latest version

	```
	git clone https://github.com/GerardBalaoro/ThemeForge.git
	```

- Install required Python packages.

	```
	pip install -r packages.txt
	```

- Execute entry script.

	```
	python forge.py -h
	```


## Building Binaries Using PyInstaller

- Intall PyInstaller

  ```
  pip install pyinstaller
  ```
  
- Windows

  ```
  pyinstaller forge.py -F -i icons/win.ico --name "ThemeForge"
  ```

- MacOS

  ```
  pyinstaller forge.py -F -i icons/mac.icns --name "ThemeForge"
  ```


## Credits

- Icon made by [Darius Dan](https://www.flaticon.com/authors/darius-dan) from [www.flaticon.com](https://www.flaticon.com/) is licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)
