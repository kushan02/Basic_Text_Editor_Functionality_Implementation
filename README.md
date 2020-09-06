###Contents:
1. Usage
2. Results
3. Overview
4. Analysis of the Existing Solution (Arrays)
5. Performance Enhancement
6. Different Approaches to Performance Improvement
    1. List of possible approaches
    2. Ropes
    3. Gap Buffer
    4. Doubly Linked List (Preferred approach)
7. Ideas for sophisticated implementation
8. Suggestions for Searching and Spell-Check
9. The Benchmarking Setup
10. References

### Usage

No extra 3rd party library is used for the implementation. The execution and benchmarking is done in the same way as given in the boilerplate code.

Although multiple test files have been added and each one can be used to benchmark it. In the solution implemented, we have tested for all three kinds of usage scenario: small, medium, and long text files.

Run using:
`python3 editor.py`

**NOTE**: The biggest change compared to the original implementation is that instead of character by character operations, I have used word by word operations. 

Although letter wise operations are completely feasible to be implemented, it would require some additional sophistication in coding, which would be a bit more time consuming for this task. 

But, the idea is really simple, for each word, just break down its word according to length (this would only be required on the two word ends bounded by the character count to copy)

To offset for the difference in character count that would have operation performed on, I have added an multiplication factor 5 as the average word length. That would make up for any difference in benchmark performance between Simple and Enhanced versions.

The test cases have been generated by `test_case_generator.py` file, which randomizes the word count of each file and fills it with random strings of length 1 to 10. It has been divided into short, medium and long data sets. Each type consist of 10 test files.

### Results

(Putting up the results before the entire thought process write up to save time)

**Large sized data set**
>Cut Paste Time is faster in Enhanced version by 71944.48%
>>(2.60801s vs 0.00362s)

>Copy Paste Time is faster in Enhanced version by 55237.03%
>>(2.4957s vs 0.00451s)

>Get text Time is faster in Simple version by 140.0%
>>(0.0006s vs 0.00025s)

>Misspelling time is faster in Enhanced version by 126172334.62%
>>(328.04833s vs 0.00026s)

---
**Medium sized data set**:
>Cut Paste Time is faster in Enhanced version by 3949.24%
>>(0.13322s vs 0.00329s)

>Copy Paste Time is faster in Enhanced version by 1632.27%
>>(0.08159s vs 0.00471s)

>Get text Time is faster in Simple version by 128.0%
>>(0.00057s vs 0.00025s)

>Misspelling time is faster in Enhanced version by 13872624.0%
>>(34.68181s vs 0.00025s)

---
**Small sized data set**
>Cut Paste Time is faster in Simple version by 70.29%
>>(0.00298s vs 0.00175s)

>Copy Paste Time is faster in Simple version by 196.18%
>>(0.00465s vs 0.00157s)

>Get text Time is faster in Simple version by 103.57%
>>(0.00057s vs 0.00028s)

>Misspelling time is faster in Enhanced version by 74911.54%
>>(0.19503s vs 0.00026s)
---

One of the main points kept in mind while designing the architecture of all the modules is that we would be dealing with files that would contain data usually from few hundred KBs to few MBs.

We see that our new implementation out performs the original naive implementation by many folds.

Although, while in small test cases, the naive implementation comes at top. This is simply due to the fact that the nuances of our current implementation cause an overhead compared to the smaller execution time for simple array operations for very small files. So although, our solution turns out to be slower but it is in the orders of magnitude negligible to any system (difference is a couple ms).

The get text seems a bit slow on our implementation, but rather it has massive benefits that it uses python generator instead of loading the entire text file into memory at once.

Our new solution, starts shining as the size of the file begins to grow by an increase in performance

**PS**: I didn't originally intend to write-up this long documentation, but I really loved the concept you guys have come up with and this particular task was very interesting to me so it went a bit in detail. Kudos to the team!

### Overview

The first step should be to understand the existing implementation and try to figure out how the operations provided works under the hood. The next step then will be to figure out the time complexity of the operations that occur that would give us an better idea about the bottlenecks we are facing and try finding the answer to the eternal question in the CS world, "Can we do better?"

Then we need to do our homework well and study the existing real-life solutions if any, and learn more about the nuances of the problem statement. The last step, would then be to improvise on the research findings and perform various benchmarks covering test cases that are very likely to cause a bottle neck for stress testing our modules. At the same time, a real-life like simulation is also essential to ensure that the stress testing doesn't lead us to over-engineering of our solution. A balance between both will yield a perfectly viable solution that we can choose for our project.

### Analysis of the Existing Solution (Arrays)

On taking a bird's eye view of the current task at hand, we identify 4 major functionality we are trying to provide the end user with:
 
1. Cut
2. Copy
3. Paste
4. Spell Check
5. Deletion (In simple words, a cut operation with no paste)

**Cut Operation**: The current solution invokes a fresh copy of the document string each time a cut operation is performed, leading to a cost overhead by copying over all the old data by removing the range of blob text. This new string thus created, now acts as the document text. But, before the creation of the document, the selected text is stored into a temporary string buffer (variable) which is used to preserve the data in the clipboard at any instance of time

- *Time Complexity => O(n)*

**Copy Operation**: The copy operation stores the selected range of text blob into the buffer variable mentioned above for storing paste data

- *Time Complexity => O(m)*

**Paste Operation**: The data stored inside our string buffer that was feed in during cut or copy operation is finally utilized to insert the data at the given location. For this, string concat operation is performed, which leads to copying and shifting of all the data again.

- *Time Complexity => O(n + m)*

- (n is the length of the document, m is the length of paste data)

**NOTE**: Strings in Python are immutable objects under the hood, that means any manipulation operation on strings will have a overhead of copying over the old data and creating a new instance.

### Performance Enhancement

In the previous section, on analysis it becomes very quickly evident that using strings for storing the data is clearly not the best way to go about it. This is due to the fact that manipulation operations on immutable objects usually tend to be very expensive.

Also, one more analysis is overlooked, that is the cost of adding new content. In text editors, users type couple of new characters every second and deletions are also very frequent. This new addition would lead to lots of shifting of data causing very poor performance. Similar time and memory problems would be faced when we use an array instead of string (if we emphasise the intricate details, a string is simply an array of characters per se). These methods are clearly not feasible and can be dismissed as options rather quickly.

Therefore, we need to think in the direction of storing our document as some form of mutable structure.

On researching more about this problem, a well written paper by Charles Crowley - "The Craft of Text Editing" helps suggest multiple approaches with which this problem can be tackled. Also, on further doing the analysis of the existing solutions already available in the market, there are also a couple of more sophisticated approaches that many have taken.

### Different Approaches to Performance Improvement

The below are the various approaches to attack the problem (discussing each one is detail would be out of scope for this use case):

1. Arrays
2. Doubly Linked Lists
2. Buffer Gap
3. Linked Line
4. Page Buffer Gap
5. Piece Table
6. Ropes
7. Zippers

While we won't go into details for each of the following approaches, here is an excerpt from Charles's book (while it doesn't cover ropes, we shall see it in brief):

> Use the buffer gap method if at all possible.

> Only use the linked line method if you are implementing in an environment that likes to manipulate lists of small objects; for example, Lisp environments.

> Only use the paged buffer gap method if resources are tight.

*Real-world examples*:
- Emacs - Gap Buffer (One of the best available text editors)
- MS Word - Piece Table (Industry Standard for word document processing)
- Sam Editor - Ropes (Large text editing capabilities)

#### Ropes

> A rope is a binary tree where each leaf (end node) holds a string and a length (also known as a "weight"), and each node further up the tree holds the sum of the lengths of all the leaves in its left subtree. A node with two children thus divides the whole string into two parts: the left subtree stores the first part of the string, the right subtree stores the second part of the string, and a node's weight is the length of the first part. 

Ropes would usually be used if we are dealing with large files and more often insertion, deletions and concat operations. The goal in our case is copy and paste. It is best suited in scenarios where concatenation is a frequent operation.

Also, it is a very complex implementation increasing the complexity of the source code by many folds, often prone to lot more bugs than its counterpart solution. (Would not recommend unless some senior developers are going to work on this segment)

The complexity v/s performance gain trade-off would usually not be worth it, unless the product is already at a stage where improvement in even slight fraction of performance is critical, only then we should think of this approach.

(A small assumption we are overlooking here is that it was mentioned that while benchmarking they found this approach to be slow compared to the traditional approach. That means they tested it for data that would usually be larger in size like couple of MBs to make the difference significant. Otherwise, for smaller blobs of text the difference would be hardly noticeable.)

#### Gap Buffer

> A gap buffer in computer science is a dynamic array that allows efficient insertion and deletion operations clustered near the same location. Gap buffers are especially common in text editors, where most changes to the text occur at or near the current location of the cursor.

A gap buffer is a generalization of an unbounded array: although an unbounded array allows for efficient insertion and deletion of elements from the end, a gap buffer allows for efficient
insertion and deletion of elements at the middle.

>A gap buffer attempts to avoid the cost of shifting by placing the empty portion of the
array somewhere within the array. Hence the name “gap buffer" referring to the “gap" within
the “buffer". The gap is not fixed to any one position. At any time it could be at the halfway
point of the buffer or just at the beginning or anywhere in the buffer. We can immediately
see the potential benefits of this approach.

When the user moves the cursor in the text editor, the implementation automatically
moves the gap, thereby providing the unused portion of the array to be used for possible insertions.
 
 In the worst case scenario we have to move the gap from the beginning of the text file to the end. But if subsequent operations are only a few indexes apart, we will get a lot better performance compared to using a dynamic array.

One assumption we are considering as a reason for not using Gap Buffers in our use case is we are not told about the frequency of pasting and the length of the text that is selected for pasting. 

In practical scenarios, it is often safe to assume a good enough size of the gap buffer, but in this case it is unclear what type of use case we are dealing with. For instance, if the major use case is copying and pasting large log files, then the usage of gaps makes little sense as it would add up to lot of overhead for extra memory. Also, gap buffers work with contiguous allocation of memory; and, in this case we do not know the size of the files we are dealing with and the resource constraints. So, although, gap buffer is usually used in real-world applications, it is mostly never used as it is without knowing the exact use case scenario; it is always coupled with some sophisticated implementations (one such is suggested in the next section).

Last thing is, for this particular task, our major focus is on Cut, Copy, Paste operations, where the below solution has the potential to yield better results.

#### Doubly Linked Lists (Preferred approach)

After some brainstorming, doubly linked list is the ideal data structure that comes to mind after dismissal of the idea of arrays. While seemingly pretty promising, there is one flaw with this approach, that causes this data structure to miss to become the ideal data structure for used standalone in a fully function text editor. 

> A doubly linked list is a linked data structure that consists of a set of sequentially linked records called nodes. Each node contains three fields: two link fields (references to the previous and to the next node in the sequence of nodes) and one data field. The beginning and ending nodes' previous and next links, respectively, point to some kind of terminator, typically a sentinel node or null, to facilitate traversal of the list.

The power of the linked list lies in the fact, that insertion and deletions are constant time operations. Also, biggest advantage is that we don't have to allocate contiguous memory to store the document data.

But, the biggest downside is that, random access is not possible in linked lists. We often need to traverse from the beginning of the list to reach the desired index.

But, even Gap Buffer works on the assumption that usually people would make edits nearby the cursor and hence it is effective for most real-world applications as this is often true. If the user switches to the first word of the text from last word, then even in the case of Gap Buffers we are looking at the worst time complexity of O(n).

So, assuming that generally we also move the cursor to the place where we want to place it compared to directly jumping to some another part of text; Linked lists, actually fare pretty well in performance.

Also, another major advantage would be the liberal usage of memory and working with even extremely large files which would otherwise not be possible while using any dynamic arrays (contiguous memory allocation) type implementations.

One instance of clear advantage of linked list, over Gap Buffer implementation is the major cost reduction in cut and paste operation. Actual copying, deleting and then pasting would take considerable time for large chunks. But, in this case it would be possible in O(1) time provided we know the exact locations before-hand. Because cutting and pasting simply would be re-linking that part of the list to some another segment.

The deletion operation would also be very quick as it can be done in O(1) time complexity as it just involves de-linking the selected segment from the entire list of nodes.

We are also adding a nice trick called Copy Deferral. This means that as soon as some sort of copy operation is specified, we don't immediately actually copy into the paste buffer, rather, we don't commit the operation unless compulsorily required.

For instance, say we performed a copy operation and we issued a deferral. The benefits of this are:
- If another cut operation follows right after the former copy operation, the paste buffer will anyways be overwritten by the selected cut text (and cut text in case of our implementation is very quick as it doesn't involve actual copying, but just rearrangement of pointers)
- If another copy operation follows right after the former copy operation, we can avoid the overhead of previous copy as the paste buffer is anyways overwritten
- If a paste operation is performed, then the relative order in which the earlier copied text is remains the same. We just need to adjust the pointers to the newly created chains at the endpoints (things would change slightly if there were edit operations, where we would need to monitor the position between (i,j) and if any changes are detected commit the copy operation to memory before allowing any modifications.

As we observe in only one instance an actual copying mechanism is required.

So now, most of our operations are constant time in nature with just the overhead of pasting the actual blob text selected in O(m), but this operation is inevitable, and hence we are at a pretty good standing with this implementation

**NOTE**: The biggest, yet practically sensible assumption we are making is that the operations involved would usually occur in the proximity of where the cursor is, that means we usually get to our desired index pretty quickly on average often times not causing the worst case to trigger.

(So in the code here, we have used indexes that acts as the current cursor location so we can simulate a more real-world scenario.

To make things simple, we are also assuming that these indexes refer to the word itself and not letters. In the latter case, the implementation would get much more sophisticated and tricky, but completely doable given ample time.

### Ideas for sophisticated implementation

A combination of linked lists and gap buffer can be used; doubly linked list where each node contains a specific size of gap buffer. The contents of a text file represented in this way is simply the concatenation of the contents of each gap buffer in the linked list.
 
 Also, to tackle the issue of random access; we can maintain a lookup table that stores the starting address of each new paragraph or significant blobs of text and the range and character count. Updating the range alone would be easier and for practical purposes traversing entirely through a paragraph would not be expensive even in worst case assuming normal sized-chunks of paragraphs.
 
 We can also add stacks and define reverse of each operations so we can perform undo and redo operations.
 
 We are also not implementing delete operation here, which would be simply the cut operation without pasting any data.
 
 Also, instead of storing each word as a node, we could dynamically decide the size of grouping of text, i.e. maybe store the entire node as a line of text, or in some cases even paragraph or some cases a bi-gram or tri-gram. This thing requires a proper amortized analysis of operation cost to determine a better approach.
 
 ### Suggestions for Searching and Spell-Check
 
 One bottleneck in the spell checking implementation of the provided version is that spell check is performed each time on the entire document. This approach is clearly infeasible as we see for bigger iterations of benchmarking, it can easily take hours to yield results.
 
 A simple solution for this would be to do it only once, and at the time document is created or as and when a new word is insert.
 
 A more sophisticated solution would be to do this in the local proximity of where changes have occurred after performing any operation as an background asynchronous task. This would ensure that we don't miss out on any spelling errors. (This would be very complicated to implement and beyond the scope of this task) 
 
 For an enhanced way to performing spell check, the answer depends upon the functionalists required in Spell Checker and availability of memory. Hashing is one simple option for this. We can put all words in a hash table and simply look up each word present. The current implementation is good enough with time complexity of O(n log m) . If we want both operations, look up and prefix search, Trie is suited. With Trie, we can support all operations like insert, search, delete in O(n) time where n is length of the word to be processed. Another advantage of Trie is, we can print all words in alphabetical order which is not possible with hashing. 
 
 For showing auto-suggestions for fixing the spelling errors we can calculate the Damerau–Levenshtein distance for finding a close match to the misspelled word. 
 
 A Heuristic based approach would be more efficient as the naive brute force approach would be pretty slow. 
 
 The idea is to look at the types of spelling errors people make, and to design hash functions that would assign an incorrect spelling to the same bucket as its correct spelling.

> For example, a common mistake is to use the wrong vowel, like definate instead of definite. So you design a hash function that treats all vowels as the same letter. An easy way to do that is to first "normalize" the input word and then put the normalized result through a regular hash function. In this example, the normalizing function might drop all the vowels, so definite becomes dfnt. The "normalized" word is then hashed with a typical hash function.


###The Benchmarking setup:

 We are using a python library called timeit (present with the boilerplate code) which provides a simple way to time small bits of Python code. This is how we get an approximate idea about how our modules are performing with respect to the test data.

We pass in the test data and the iterations for which we want to perform benchmark. 

We have not made any major change in the way benchmarking works.
 
 ### References
 - https://stackoverflow.com/questions/4046246/how-are-text-editors-generally-implemented
 - https://www.averylaird.com/programming/the%20text%20editor/2017/09/30/the-piece-table/
 - https://news.ycombinator.com/item?id=15381886
 - https://www.cs.cmu.edu/~wjh/papers/byte.html
 - http://www.finseth.com/craft/index.html
 - https://www.geeksforgeeks.org/gap-buffer-data-structure/
 - https://en.wikipedia.org/wiki/Gap_buffer
 - https://web.ics.purdue.edu/~elgamala/ECE368/cp6.pdf
 