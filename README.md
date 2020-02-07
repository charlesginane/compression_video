# Compression video

## Introduction

Le but de ce projet est de présenté une application permettant le décodage de flux mpeg-2
et d'en créer une application.

Cette application est écrite en langage Python en version 3.


## Requirements

Les packages requis pour l'applications sont:
* numpy
* matplotlib
* scikit-image
* opencv2
* tqdm

Le fichier requirements.txt permet de lister les packages Python utilises pour notre application.
Pour s'en servir, il suffit de faire la commande suivante à condition d'avoir pip d'installé:

```bash
pip install -r requirements.txt
```

Il faut bien le tool **mpeg2dec** afin de pouvoir l'utiliser. Il doit être placer
à la racine afin qu'il puisse être utiliser par l'application

Afin de pouvoir récuperer la version modifié de mpeg2dec, le script `get_mpeg2dec.sh` permet de le télécharger et le compiler dans le dossier *tools*.

## Utilisation

### En cas de besoin

La liste des options est disponibles à l'aide de l'option **--usage** et **--help** comme ceci:
```
./main.py --help
```

Cette commande nous affiche:

```
./main.py -s -p pid --fps <Number of FPS> --pgm <PGM image> --decompress <Video file>

-s: Save mode
   Save the video in a file
-p: Pid of video
   Specify a pid for a video
--fps: frame sequence
   Specify the frame sequence of the video which will be generated
--decompress: the video
   Specify the video which will be decomrpessed
```

### Utilisation simple

POur décoder une vidéo, il suffit d'utiliser l'option **--decompress** suivi du flux vidéo à décoder. Ci dessous, un exemple avec la vidéo *lci.m2v*:

```
/main.py --decompress ../videos/elementary/lci.m2v
```

L'application va alors décoder la vidéo, sauvegarder la pile d'image dans le dossier *workspace/tmp/* et convertir toutes ces images dans le dossier *workspace/res/*. Enfin, la vidéo sera affichée à l'écran.

On peut sauvegarder la vidéo à l'aide de l'option **-s** comme ceci:

```
/main.py -s --decompress ../videos/elementary/pendulum.m2v
```

le fichier *out.mp4* sera alors créer et contiendra la vidéo.

### Options plus poussées

#### FPS

On peut spécifier la cadence d'images par seconde (fps) à l'aide de l'option **--fps**. Cette option va permettre de forcer la cadence de la vidéo. On l'utilise comme ceci avec une cadence à 25 fps:

```
/main.py --fps 25 --decompress ../videos/elementary/pendulum.m2v
```

#### pid

On peut spécifier un pid d'une vidéo avec l'option **--pid** comme montrer dans l'example ci-dessous (pid à 0x3fd):

```
./main.py -s --pid "0x3fd" --decompress ../../videos/ts/ctv.ts
```

### Les résultats

L'application va créer:
* Le fichier log.txt qui regroupe les flags de mpeg2dec déclenchés lors du décodage
* Le dossier workspace/tmp qui regroupe l'ensemble des images décoder par mpeg2dec
* Le dossier workspace/res qui regroupe l'ensemble des frames désentrelacés et en RGB
* La vidéo out.mp4 si l'option **-s** est activé

### Architecture

|- README.md              # Ce fichier
|- get_mpeg2dec.sh        # Script pour obtenir mpeg2dec
|- main.py                # Le script principale
|- src/
|  |- tool.py             # Ce fichier regroupe les fonctions pour notre application
|  |- lib/
|     | image.py          # Gestion de l'image et du désentrelacement
|     | decompression.py  # Wrapper du tool mpeg2dec
