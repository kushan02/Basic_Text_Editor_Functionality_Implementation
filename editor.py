import random


class SimpleEditor:
    def __init__(self, document):
        self.document = document
        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = ""

    def cut(self, i, j):
        self.paste_text = self.document[i:j]
        self.document = self.document[:i] + self.document[j:]

    def copy(self, i, j):
        self.paste_text = self.document[i:j]

    def paste(self, i):
        self.document = self.document[:i] + self.paste_text + self.document[i:]

    def get_text(self):
        return self.document

    def print_text(self):
        print(self.get_text())

    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result


class EnhancedEditor:
    # Doubly Linked List data structure to store the entire document as chain of words

    class Word:
        def __init__(self, text=None, next=None, prev=None):
            self.text = text
            self.next = next
            self.prev = prev

    def __init__(self, document):

        self.document_head = None
        self.document_tail = None

        # The cursor is the current position where we want to execute any operation
        self.document_cursor = None

        self.word_count = 0

        for word in document.split():
            # Initialize the word chain if it is the first to be processed
            if self.document_head is None:
                self.document_head = self.document_tail = EnhancedEditor.Word(word)
            # Else extend the chain of lists by a new word
            else:
                # Create a new word whose prev points to the last word
                new_word = EnhancedEditor.Word(text=word, prev=self.document_tail)
                # Update the next of last word to point to the new word
                self.document_tail.next = new_word
                # Update tail to point to the new word
                self.document_tail = new_word

            self.word_count += 1

        self.dictionary = set()
        # On windows, the dictionary can often be found at:
        # C:/Users/{username}/AppData/Roaming/Microsoft/Spelling/en-US/default.dic
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)

        self.paste_head = None
        self.paste_tail = None

        # Flag for disabling the default behavior to defer copy operation
        # by avoiding useless copy operations to the paste buffer
        self.copy_deferral_override = False
        self.copy_deferred_boundary = (0, 0)
        self.paste_blob_length = 0

        self.is_last_operation_copy = False

        # Perform spell check in the beginning to avoid doing it each time for entire document
        self.misspelled_word_count = 0
        self.preprocess_misspellings()

    def set_cursor(self, index):
        # This is done as a assumption that we would always do the operations in proximity of our cursor
        # Thus, causing the worst case to rarely execute
        word_count = 1
        self.document_cursor = self.document_head
        while word_count < index:
            self.document_cursor = self.document_cursor.next
            word_count += 1

    def cut(self, i, j):
        # We are using the format [i, j)
        if i >= j:
            return

        self.is_last_operation_copy = False

        # Bring the cursor at index i
        self.set_cursor(i)
        self.copy_deferred_boundary = (0, 0)
        self.paste_blob_length = j - i

        self.word_count -= (j - i)
        paste_selected_word_count = 0
        while paste_selected_word_count < j - i and self.document_cursor is not None:
            if paste_selected_word_count == 0:
                self.paste_head = self.document_cursor
            self.paste_tail = self.document_cursor
            self.document_cursor = self.document_cursor.next
            paste_selected_word_count += 1

        # Properly initialize null values on endpoint on the pasted chain of words
        if self.document_cursor is not None:
            self.document_cursor.prev.next = None

        # Remove the selected cut words from selection
        last_word_before_cut_selection = self.paste_head.prev
        # If the paste selection includes the first word too, there is no word preceding it
        if last_word_before_cut_selection is None:
            self.document_head = self.document_cursor
            if self.document_cursor is not None:
                self.document_cursor.prev = None
        else:
            last_word_before_cut_selection.next = self.document_cursor
            if self.document_cursor is not None:
                self.document_cursor.prev = last_word_before_cut_selection

        # Properly initialize null values on starting on the pasted chain of words
        self.paste_head.prev = None

    def copy(self, i, j):
        if i >= j:
            return

        self.is_last_operation_copy = True

        self.set_cursor(i)

        self.paste_head = self.document_cursor
        self.paste_blob_length = j - i
        self.copy_deferred_boundary = (i, j)

    def paste(self, i):
        if i > self.word_count:
            return

        self.set_cursor(i)

        if self.document_cursor.next is not None:
            last_word = self.document_cursor.next
        else:
            last_word = None

        # We only need to create a copy in case our previous operation was a copy operation
        # In case the previous operation was a cut operation, we simply relink that chain with the current chain
        if self.is_last_operation_copy:
            self.set_cursor(self.copy_deferred_boundary[0])
            paste_count = 0
            while paste_count < self.paste_blob_length and self.document_cursor is not None:
                if paste_count == 0:
                    self.paste_head = EnhancedEditor.Word(self.document_cursor.text, prev=None,
                                                          next=self.document_cursor.next)
                    self.paste_tail = self.paste_head
                else:
                    self.paste_tail.next = EnhancedEditor.Word(self.document_cursor.text, prev=self.paste_tail,
                                                               next=self.document_cursor.next)

                    self.paste_tail = self.paste_tail.next

                paste_count += 1
                self.document_cursor = self.document_cursor.next

        self.set_cursor(i)
        self.document_cursor.next = self.paste_head
        self.paste_head.prev = self.document_cursor
        last_word.prev = self.paste_tail
        self.paste_tail.next = last_word

    def get_text(self):
        # We are using a generator object for avoiding memory constraints when dealing with large texts
        pointer = self.document_head
        while pointer is not None:
            yield pointer.text + " "
            # print(pointer.text, end=" ")
            pointer = pointer.next

    def print_text(self):
        print("".join([x for x in self.get_text()]))

    def preprocess_misspellings(self):
        pointer = self.document_head
        while pointer is not None:
            if pointer.text not in self.dictionary:
                self.misspelled_word_count += 1
            pointer = pointer.next

    def misspellings(self):
        return self.misspelled_word_count


import timeit


class EditorBenchmarker:
    new_editor_case = """
from __main__ import {}
s = {}("{}")"""

    editor_cut_paste = """
for n in range({}):
    if n%2 == 0:
        s.cut(1, {})
    else:
        s.paste(2)"""

    editor_copy_paste = """
for n in range({}):
    if n%2 == 0:
        s.copy(1, {})
    else:
        s.paste(2)"""

    editor_get_text = """
for n in range({}):
    s.get_text()"""

    editor_mispellings = """
for n in range({}):
   s.misspellings()"""

    def __init__(self, cases, N, editor_type="SimpleEditor"):
        self.cases = cases
        self.N = N

        cut_paste_range = 3
        if editor_type == "SimpleEditor":
            cut_paste_range *= 5

        self.editor_cut_paste = self.editor_cut_paste.format(N, cut_paste_range)
        self.editor_copy_paste = self.editor_copy_paste.format(N, cut_paste_range)
        self.editor_get_text = self.editor_get_text.format(N)
        self.editor_mispellings = self.editor_mispellings.format(N)

        # Add an option to benchmark in different editor modes: simple and enhanced
        # So we can easily contrast the results
        self.editor_type = editor_type

    def benchmark(self):
        avg_cut_paste_time = avg_copy_paste_time = avg_get_text_time = avg_mispellings_time = 0

        for case in self.cases:
            print("Evaluating case of length = {} by {} editor:".format(len(case), self.editor_type))
            new_editor = self.new_editor_case.format(self.editor_type, self.editor_type, case)
            cut_paste_time = timeit.timeit(stmt=self.editor_cut_paste, setup=new_editor, number=1)
            print("{} cut paste operations took {} s".format(self.N, cut_paste_time))
            copy_paste_time = timeit.timeit(stmt=self.editor_copy_paste, setup=new_editor, number=1)
            print("{} copy paste operations took {} s".format(self.N, copy_paste_time))
            get_text_time = timeit.timeit(stmt=self.editor_get_text, setup=new_editor, number=1)
            print("{} text retrieval operations took {} s".format(self.N, get_text_time))
            mispellings_time = timeit.timeit(stmt=self.editor_mispellings, setup=new_editor, number=1)
            print("{} mispelling operations took {} s".format(self.N, mispellings_time))

            avg_cut_paste_time += cut_paste_time
            avg_copy_paste_time += copy_paste_time
            avg_get_text_time += get_text_time
            avg_mispellings_time += mispellings_time

        return (round(avg_cut_paste_time / len(self.cases), 5), round(avg_copy_paste_time / len(self.cases), 5),
                round(avg_get_text_time / len(self.cases), 5), round(avg_mispellings_time / len(self.cases), 5))

    @staticmethod
    def load_large_data_files():
        test_data = []
        # Due to the large time required for testing, we are testing only 1 big test file
        # If you have more than 10 mins for each test case then you can go ahead with adding more files
        with open("tests/large/test_large_{}.txt".format(random.randint(0, 9)), 'r') as file:
            test_data.append(file.read().replace('\n', ''))
        # for i in range(0, 10):
        #     with open("tests/large/test_large_{}.txt".format(i), 'r') as file:
        #         test_data.append(file.read().replace('\n', ''))
        #
        return test_data

    @staticmethod
    def load_medium_data_files():
        test_data = []
        for i in range(0, 10):
            with open("tests/medium/test_medium_{}.txt".format(i), 'r') as file:
                test_data.append(file.read().replace('\n', ''))

        return test_data

    @staticmethod
    def load_small_data_files():
        test_data = []
        for i in range(0, 10):
            with open("tests/small/test_small_{}.txt".format(i), 'r') as file:
                test_data.append(file.read().replace('\n', ''))

        return test_data


if __name__ == "__main__":

    TEST_ITERATIONS = 1000

    # Load files using either: small, medium or large files
    test_data = EditorBenchmarker.load_medium_data_files()

    b_simple = EditorBenchmarker(test_data, TEST_ITERATIONS, editor_type="SimpleEditor")
    simple_cut_paste_time, simple_copy_paste_time, simple_get_text_time, simple_mispellings_time = b_simple.benchmark()

    print("================================")

    b_enhanced = EditorBenchmarker(test_data, TEST_ITERATIONS, editor_type="EnhancedEditor")
    enhanced_cut_paste_time, enhanced_copy_paste_time, enhanced_get_text_time, enhanced_mispellings_time = b_enhanced.benchmark()

    print("\n==============================")

    print("Results:")

    if simple_cut_paste_time > enhanced_cut_paste_time:
        print("Cut Paste Time is faster in Enhanced version by {}%".format(
            round((simple_cut_paste_time - enhanced_cut_paste_time) / enhanced_cut_paste_time * 100, 2)))
        print("({}s vs {}s)".format(simple_cut_paste_time, enhanced_cut_paste_time))
    else:
        print("Cut Paste Time is faster in Simple version by {}%".format(
            round((enhanced_cut_paste_time - simple_cut_paste_time) / simple_cut_paste_time * 100, 2)))
        print("({}s vs {}s)".format(enhanced_cut_paste_time, simple_cut_paste_time))

    if simple_copy_paste_time > enhanced_copy_paste_time:
        print("Copy Paste Time is faster in Enhanced version by {}%".format(
            round((simple_copy_paste_time - enhanced_copy_paste_time) / enhanced_copy_paste_time * 100, 2)))
        print("({}s vs {}s)".format(simple_copy_paste_time, enhanced_copy_paste_time))
    else:
        print("Copy Paste Time is faster in Simple version by {}%".format(
            round((enhanced_copy_paste_time - simple_copy_paste_time) / simple_copy_paste_time * 100, 2)))
        print("({}s vs {}s)".format(enhanced_copy_paste_time, simple_copy_paste_time))

    if simple_get_text_time > enhanced_get_text_time:
        print("Get text Time is faster in Enhanced version by {}%".format(
            round((simple_get_text_time - enhanced_get_text_time) / enhanced_get_text_time * 100, 2)))
        print("({}s vs {}s)".format(simple_get_text_time, enhanced_get_text_time))
    else:
        print("Get text Time is faster in Simple version by {}%".format(
            round((enhanced_get_text_time - simple_get_text_time) / simple_get_text_time * 100, 2)))
        print("({}s vs {}s)".format(enhanced_get_text_time, simple_get_text_time))

    if simple_mispellings_time > enhanced_mispellings_time:
        print("Misspelling time is faster in Enhanced version by {}%".format(
            round((simple_mispellings_time - enhanced_mispellings_time) / enhanced_mispellings_time * 100, 2)))
        print("({}s vs {}s)".format(simple_mispellings_time, enhanced_mispellings_time))

    else:
        print("Misspelling is faster in Simple version by {}%".format(
            round((enhanced_mispellings_time - simple_mispellings_time) / simple_mispellings_time * 100, 2)))
        print("({}s vs {}s))".format(enhanced_mispellings_time, simple_mispellings_time))
