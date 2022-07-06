#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>
#define MAX 200

const char INFILE[]="dijkstraData.txt";
struct EDGE        {
  long vertex;
  long weight;
  struct EDGE *next;
};
void fetch_g(struct EDGE **g)        {
  FILE *fp = fopen(INFILE,"r");
  long i,v,w;
  char *token,line[800];
  struct EDGE *node;
  while (fgets(line,800,fp))        {
        token = strtok(line,"\t");
        i = atoi(token);
        g[i] = malloc(sizeof(struct EDGE));
        g[i]->next = NULL;
        while (token = strtok(NULL,"\t\r\n"))        {
                sscanf(token,"%ld,%ld",&v,&w);
                node = malloc(sizeof(struct EDGE));
                node->vertex = v;
                node->weight = w;
                node->next = g[i]->next;
                g[i]->next = node;
        }
  }
}
void print_g(struct EDGE *g)        {
  struct EDGE *node;
  for (node=g; node->next; node=node->next)
        printf("%ld,%ld\t",node->next->vertex,node->next->weight);
  printf("\n");
}
void HEAP_DECREASE_KEY(long *q,long i,long *d)        {
  long tmp;
  while ((i>1) && (d[q[i/2]]>d[q[i]]))        {
        tmp = q[i];        q[i] = q[i/2]; q[i/2] = tmp;
        i = i/2;
  }
}
void INIT_SINGLE_SOURCE(struct EDGE **g,long s,long *d,long *p)        {
  long i;
  for (i=1; i<=MAX; i++)        {
        d[i] = 1000000;                //        d[i] = INFINITY
        p[i] = -1;                        //        p[i] = NIL
  }
  d[s]=0;
}
void MIN_HEAPIFY(long *q,long i,long *d)        {
  long left = 2*i, right = 2*i+1, smaller, tmp;
  if ((left<=q[0])&&(q[left]<q[i]))
        smaller = left;
  else
        smaller = i;
  if ((right<=q[0])&&(q[right]<q[smaller]))
        smaller = right;
  if (smaller != i)        {
        tmp = q[smaller]; q[smaller] = q[i]; q[i] = tmp;
        MIN_HEAPIFY(q,smaller,d);
  }
}
long EXTRACT_MIN(long *q, long *d)        {
  long min = q[1];
  q[1] = q[q[0]--];
  MIN_HEAPIFY(q,1,d);
  return min;
}
void REFRESH(long u,struct EDGE **g,long *d,long *p)        {
  struct EDGE *node;
  long v,w;
  for (node=g[u]; node->next; node=node->next)        {
        v = node->next->vertex;
        w = node->next->weight;
        if (d[u]+w<d[v])        {
          d[v]=d[u]+w;
          if (p[v]==(-1))
                p[v]=u;
          else
                REFRESH(v,g,d,p);
        }
  }
}
void Dijkstra(struct EDGE **g, long s)        {
  long *d,*p,*q,i,u;
  struct EDGE *node;
  d = calloc(MAX+1,sizeof(long));
  p = calloc(MAX+1,sizeof(long));
  q = calloc(MAX+1,sizeof(long));
  q[0] = MAX;
  for (i=1; i<=MAX; i++)
        q[i] = i;
  INIT_SINGLE_SOURCE(g,s,d,p);
  while (q[0])        {
        u=EXTRACT_MIN(q,d);
        REFRESH(u,g,d,p);
  }
  printf("%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld,%ld\n",d[7],d[37],d[59],d[82],d[99],d[115],d[133],d[165],d[188],d[197]);
}
void main()
{
  struct EDGE **g;
  g = (struct EDGE **)calloc(MAX+1,sizeof(struct EDGE *));
  fetch_g(g);
  Dijkstra(g,1);
}