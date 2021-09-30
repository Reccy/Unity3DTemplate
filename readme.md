# Unity 3D Template

This is a simple template for getting started with a Unity project quickly. The purpose of this template is for personal use, so I won't be able to provide support if you decide to use this template for yourself.

## Template Initialization
1. Clone the repo to an empty directory
2. Add the project to the Unity Hub and then open it
3. Install paid assets through package manager:
 1. Rewired (https://assetstore.unity.com/packages/tools/utilities/rewired-21676
 2. Shapes ()
4. In the project root directory, run the following command: `./init_template.sh`
5. Change the project title in `Build Settings -> Player Settings -> Product Name`
6. Change the git remote origin with `git remote set-url origin https://somenewgitrepo.git`

## Directory Layout
`/Lib` contains common submodules that are pulled from GitHub. For example, script extensions.

`/Game` is where the scripts and assets specific to the current game being made will be placed.
