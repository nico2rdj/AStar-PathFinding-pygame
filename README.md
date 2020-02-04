# AStar-PathFinding-pygame

<p align="center" >
   <a href="">
    <img alt="" src="https://media.giphy.com/media/cgfCdqzts6nqZKS5Ad/giphy.gif" width="510" height="510" />
 </a>

</p>

<h3 align="center">
  🔍 AStar-PathFinding-pygame
</h3>
<p align="center">
  Algorithme A* sur l'interface Pygame  <br/>
  <small></small>
</p>

## Manuel d'utilisation

- Lancer la commande "python Base-AStar-PathFinding.py"
- b : Placer les obstacles sur la grille avec les clics de la souris
- n : Placer le point de départ du chemin sur la grille
- q / esc : Quitter l'interface pygame

## Modification de l'interface depuis le code

__sreenSize__ : Pour varier la taille de la grille <br/>
__cellSize__ : Pour varier la taille d'une case <br/>

## Détail de l'implémentation
Au niveau de A*, plusieurs structures ont été définies. <br/>
- Node : elle constitue une case du chemin sur la grille. Celle-ci est définie par trois caractéristiques. <br/>
  - g: Distance entre la case de départ et la courante
  - h: Heuristique qui est une estimation de la distance à vol d'oiseau entre le noeud courant est celui de destination
  - f: Le coût total du noeud f=g+h
- Scene : elle constitue une modélisation de la scene. L'algorithme A* est implémenté dans celle-ci. <br/>

Une brief description de A*:<br/>
- L'algorithme commence par explorer le noeud de départ en le classant comme fermé <br/>
- Il explore les noeuds autour est estiment leurs coûts <br/>
- Il regardent si les noeuds n'ont pas déjà été exploré (liste des fermés) ou en cours d'exploration (liste des ouverts) <br/>
- Check si l'un des noeuds exploré est le noeud final (si oui, on retourne le chemin trouvé en remontant les parents du noeud jusqu'à celui de départ) <br/>
- S'ils n'ont pas été exploré ou en cours d'exploration, il les ajoutent à la liste des noeuds ouverts <br/>
- Réitère tant que la liste des ouverts n'est pas nulle <br/>


## License

- [MIT](LICENSE)

## Contributors

- Nicolas Martin
