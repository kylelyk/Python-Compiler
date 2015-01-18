CFLG=-O3 -Wall

runtime.a: runtime.o hashtable.o hashtable_itr.o hashtable_utility.o
	ar -rcs $@ $^

clean:
	rm -f $(EXE) *.o *.a

runtime.o: runtime.c runtime.h
	gcc -c $(CFLG) $< -m32
hashtable.o: hashtable.c hashtable.h
	gcc -c $(CFLG) $< -m32
hashtable_itr.o: hashtable_itr.c hashtable_itr.h
	gcc -c $(CFLG) $< -m32
hashtable_utility.o: hashtable_utility.c hashtable_utility.h
	gcc -c $(CFLG) $< -m32

# Compile rules
.c.o:
	gcc -c $(CFLG) $<
