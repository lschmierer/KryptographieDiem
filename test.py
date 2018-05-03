from bruchzahlring import *

print(BruchzahlringElement(1, 3))
print(3 * BruchzahlringElement(1, 3))
print(7 * BruchzahlringElement(1, 3))
print(BruchzahlringElement(1, 3) * BruchzahlringElement(1, 3))
print(BruchzahlringElement(3, 4) + BruchzahlringElement(1, 3))
print(BruchzahlringElement(3, 4).invers())
print(-BruchzahlringElement(3, 4))
print(-BruchzahlringElement(-3, 4))
print(-BruchzahlringElement(3, -4))
print(-BruchzahlringElement(-3, -4))
