/* eslint-env node */
/**
* The file contains the edges of a directed graph. Vertices are labeled
* as positive integers from 1 to 875714. Every row indicates an edge,
* the vertex label in first column is the tail and the vertex label in
* second column is the head (recall the graph is directed, and the edges
* are directed from the first column vertex to the second column vertex).
* So for example, the 11th row looks like: "2 47646". This just means
* that the vertex with label 2 has an outgoing edge to the vertex with
* label 47646
*
* Your task is to code up the algorithm from the video lectures for
* computing strongly connected components (SCCs), and to run this algorithm
* on the given graph.
*
* Output Format: You should output the sizes of the 5 largest SCCs in the
* given graph, in decreasing order of sizes, separated by commas (avoid any
* spaces). So if your algorithm computes the sizes of the five largest SCCs
* to be 500, 400, 300, 200 and 100, then your answer should be
* "500,400,300,200,100" (without the quotes). If your algorithm finds less
* than 5 SCCs, then write 0 for the remaining terms. Thus, if your algorithm
*  computes only 3 SCCs whose sizes are 400, 300, and 100, then your answer
* should be "400,300,100,0,0" (without the quotes). (Note also that your
* answer should not have any spaces in it.)
*
* WARNING: This is the most challenging programming assignment of the course.
* Because of the size of the graph you may have to manage memory carefully.
* The best way to do this depends on your programming language and environment,
* and we strongly suggest that you exchange tips for doing this on the
* discussion forums.
*
* Download SCC.txt at:
* https://d18ky98rnyall9.cloudfront.net/_410e934e6553ac56409b2cb7096a44aa_SCC.txt?Expires=1549238400&Signature=VLryUhqjP83FRrvDK6mpb-pvpgHXD5sYWpMoBwaMrVuJk-JgtMse6NFX-ZKEFrUCsXyykR~CvAoy8fNKwceckGb1-KcDzr9bM8bFK-w2PEPDgS-m6gtSidRYz-3EUzZ6a49uZKVq0naqNZsB3neIB0nrbOAlMoDN-hDaBMYmvp4_&Key-Pair-Id=APKAJLTNE6QMUY6HBC5A
*/

// Convert text file into an adjacency list object.
const fs = require("fs");

const nodesList = [];
const g = []; // the graph as an edgesList
const adjMap = {}; // A map from node: [ list of outgoing edges for that node ]
const adjMapRev = {}; // same as adjMap, but for G_rev
let n = 0; // number of nodes
const startTime = Date.now();

try {
  var data = fs.readFileSync("SCC.txt", "utf8");
  const rows = data.split("\n");
  for (let row of rows) {
    // Remove excess white space at the end of the line
    row = row.trim();
    // Turn each row into an array
    const rowArr = row.split(" ");
    // Make edges list, convert strings to a number
    let [tail, head] = rowArr;
    tail = Number(tail);
    head = Number(head);
    // Build adjMap
    if (adjMap[tail] === undefined) {
      adjMap[tail] = [];
    }
    adjMap[tail].push(head);
    // Build adjMapRev
    if (adjMapRev[head] === undefined) {
      adjMapRev[head] = [];
    }
    adjMapRev[head].push(tail);
    g.push([ tail, head ]);
    // This simple comparison is faster than checking the entire nodesList 
    // every time with array.includes
    if (tail > n) {
      n = tail;
    }
    if (head > n) {
      n = head;
    }
  }
} catch (e) {
  console.log("Error:", e.stack);
}

// Make nodesList
for (let i = 1; i <= n; i++) {
  nodesList.push(i);
}

console.log(n);
// console.log(adjMap);
// console.log(adjMapRev);

// Implement Kosaraju's Two-Pass Algorithm to find all SCCs in O(m + n) time
// SCC = Strongly Connected Component

/**
* Intuitively, we want to first discover a "sink SCC", meaning an SCC with no
* outgoing edges. We want to discover the SCCs in "reverse topological order",
* plucking off sink SCCs one by one (AI Part 2 Section 8.6).
*
* Refresher: What do we mean by topological order? (See AI Part 2 Section 8.5.1)
* Imagine you have a bunch of tasks to complete, and there are precedence
* constraints, meaning that you cannot start some of the tasks until you have
* completed other (e.g. courses in a university degree program).
* We therefore order the vertices from the vertex with the smallest f-value to
* the one with the largest. All of G's directed edges should travel forward
* in the ordering, with the label of the tail of an edge smaller than that of
* its head.
*
* So if we want to start with a "sink SCC", then we want to start in a part of
* the graph with the largest f-value and proceed backwards (n, n - 1, ... 1) --
* hence reverse topological order.
*
* In Kosaraju's Two-Step Algorithm, the first DFS pass on G_rev finds this
* reverse topological order (we just calculate the topological order of G_rev,
* which is the same as the reverse topological order of G). This is the order
* we should process the vertices in the second DFS pass on G (starting with the
* "sink vertex" (the vertex in the last position, aka with the largest f-value)
* in the "sink SCC"), so that we uncover each SCC one at a time.
*
* Pseudocode for Kosaraju (AI Part 2 Section 8.6.4)
* Input: Directed graph G = (V, E) in adjacency list representation, with
* V = {1, 2, ... , n}.
* Postcondition: For every v, w in V, scc(v) = scc(w) iff v, w are in the same
* SCC of G.
* 1. G_rev = G with all edges reversed
* 2. Mark all vertices of G_rev as unexplored
* 3. First pass of DFS, which computes f(v)'s, the ordering
*    - TopoSort(Grev)
*      - TODO: Run this algorithm backward in the original input graph by
*        replacing the clause "each edge (s,v) in s's outgoing adjacency
*        list" in the DFS-Topo subroutine of Section 8.5.4 with "each edge
*        (s,v) in s's incoming adjacency list".
*       (Right now I am just going to create a G_rev)
*      - Should export an array that contains the vertices in order of their
*        f(v)
* 4. Second pass of DFS, finds SCCs in reverse topological order
*    - Mark all vertices of G as unexplored
*    - numSCC = 0 // global variable
*    - for each v in V, in increasing order of f(v),
*      - if v is unexplored
*        - numSCC++;
*        - Assign scc-values (details below)
*        - DFS-SCC(G,v)
*          - This is the same as DFS with one additional line of bookkeeping:
*            see pseudocode in AI Part 2 Section 8.6.4.
*/

/**
* Note: in JavaScript there is no stack limit; whereas in Python there is a
* small recursion depth (every time you recurse into a function, that adds
* another element to the stack).
*/

/**
* Takes in a directed graph, gRev, in an adjacency list representation and a
* vertex s in V. Every vertex reachable from s is marked as explored and
* has an assigned f-value.
* Note: we don't pass in gRev every time, because we aren't altering it at
* any point and can save memory by using it as a reference instead.
*/
function dfsTopo(s) {
  // mark s as explored
  explored.add(s);
  if (adjMapRev[s] === undefined) {
    return;
  }
  // For each (s,v) in s's outgoing adjacency list
  for (const head of adjMapRev[s]) {
    if (!explored.has(head)) {
      dfsTopo(head);
    }
  }
  // E.g. whichever node is first to finish being fully explored has a f(s) = 1
  finishingTime[s] = currentLabel;
  currentLabel++;
}

/**
* Takes in a directed acyclic graph, g, in adjacency list representation and
* returns the f-values of vertices that constitutes a topological ordering of g.
*/
function topoSort() {
  for (let v = n; v > 0; v--) {
    if (!explored.has(v)) {
      dfsTopo(v);
    }
  }
  // return an array with the vertices in order of their finishing times
  const finishingTimeOrder = Object.keys(finishingTime).sort((a, b) => {
    return finishingTime[b] - finishingTime[a];
  });
  // Object keys are coerced to strings, so convert them back to numbers
  return finishingTimeOrder.map((val) => {
    return Number(val);
  });
}

/**
* Takes a directed graph G = (V,E) in adjacency list representation and a
* vertex s in V.
* Marks every vertex reachable from s as "explored" and assigns it an scc-value.
* Similar to dfsTopo function. See AI Part 2 Section 8.6.5 for pseudocode of
* this function.
* Note: we don't pass in g every time, because we aren't altering it at
* any point and can save memory by using it as a reference instead.
*/
function dfsSCC(s) {
  // mark s as explored
  explored.add(s);
  scc[numSCC - 1].push(s);
  if (adjMap[s] === undefined) {
    return;
  }
  // For each edge (s,v) in s's outgoing adjacency list
  for (const head of adjMap[s]) {
    if (!explored.has(head)) {
      dfsSCC(head);
    }
  }
}

// Globals
// DFS first pass on Grev
const finishingTime = {};
let currentLabel = 1; // the first node to be fully explored is labeled 1, etc.
// Create reverse graph for first pass of DFS
const gRev = g.map(([s, v]) => {
  return [v, s];
});

// DFS both passes
const explored = new Set([]); // The list of nodes that have been explored
// DFS second pass
let numSCC = 0;
const scc =  [];

function kosaraju() {
  // First DFS pass on Grev to get the reverse topological order for the nodes
  // in G
  const reverseTopoOrder = topoSort();
  // console.log(`first DFS pass complete: order to search in second pass: ${reverseTopoOrder}`);
  // reset explored set for second DFS pass on G
  explored.clear();
  // Second DFS pass on G, traversing graph in reverse topological order
  for (const v of reverseTopoOrder) {
    if (!explored.has(v)) {
      numSCC++; // Every time we hit an unexplored node in the outer for loop, that's a new SCC
      // for easier record keeping given how they want us to submit the answer
      scc[numSCC - 1] = []; // numSCC starts at 1 but arrays index starting at 0
      dfsSCC(v);
    }
  }
  // scc is an array of arrays where the ith element represents an SCC in the
  // graph G, and each SCC is an array of the vertices contained within it.
  // e.g. [ [ 7, 1, 4 ], [ 9, 3, 6 ], [ 8, 5, 2 ] ]
  // We want to convert this into something like 3,3,3,0,0
  const result = scc.map((arr) => {
    return arr.length;
  });
  // Sort from largest to smallest SCC size, and return only the 5 largest SCCs
  return result.sort((a, b) => {
    return b - a;
  }).slice(0,5);
}

console.log(kosaraju());
const totalTime = Date.now() - startTime;
console.log(totalTime); // ms

// testCase1 answer: 3,3,3,0,0
// testCase2 answer: 3,3,2,0,0
// testCase3 answer: 3,3,1,1,0
// testCase4 answer: 7,1,0,0,0
// testCase5 answer: 6,3,2,1,0
// solution: 434821,968,459,313,211